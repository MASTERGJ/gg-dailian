#!/usr/bin/env python3
"""
Video Vision Analyzer — extract key frames from video for visual analysis.
Used as --vision mode in video_subtitle.py.

Two output modes:
  1. contact-sheet (default): Composite mosaic of key frames → single image
  2. frames: Individual key frame files + JSON manifest

Key frame extraction uses FFmpeg scene detection to capture only frames
where the visual content actually changes.

Output:
  - contact sheet image / frame files
  - manifest.json (frame list with timestamps)
  - subtitle text (for AI to merge with visual understanding)

Usage:
  python video_vision.py <URL> [--output-dir DIR] [--no-grid] [--max-frames N]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil
import time


def detect_platform(url: str) -> str:
    s = url.strip()
    if re.search(r'bilibili\.com', s) or re.match(r'^BV[a-zA-Z0-9]+$', s):
        return 'bilibili'
    if re.search(r'youtube\.com|youtu\.be', s) or re.match(r'^[a-zA-Z0-9_-]{11}$', s):
        return 'youtube'
    return 'direct'


def normalize_url(url: str, platform: str) -> str:
    """Convert BV number to full URL for Bilibili."""
    if platform == 'bilibili':
        m = re.match(r'^(BV[a-zA-Z0-9]+)$', url.strip())
        if m:
            return f'https://www.bilibili.com/video/{m.group(1)}/'
        # Already a full URL
        return url
    return url


def download_video(url: str, output_dir: str, platform: str, max_duration: int = 300) -> tuple:
    """
    Download video at lowest resolution for frame extraction.
    Returns (video_path, title, duration).
    """
    url = normalize_url(url, platform)
    print(f"Downloading video (low res) from: {url}", file=sys.stderr)
    
    import yt_dlp
    
    output_template = os.path.join(output_dir, 'video.%(ext)s')
    
    ydl_opts = {
        'format': 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'progress_hooks': [],
        'max_filesize': 104857600,  # 100MB cap
        'format_sort': ['res:480'],
    }
    
    # Bilibili needs proper headers
    if platform == 'bilibili':
        ydl_opts['http_headers'] = {
            'Referer': 'https://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
    
    # Resolution cap
    ydl_opts['format_sort'] = ['res:480', 'ext:mp4:m4a']
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First get info
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            title = info.get('title', '')
            print(f"Title: {title}", file=sys.stderr)
            print(f"Duration: {duration}s", file=sys.stderr)
            
            if duration > max_duration:
                print(f"Warning: Video is {duration}s long, limiting to first {max_duration}s", file=sys.stderr)
            
            # Download
            ydl.download([url])
    except Exception as e:
        raise RuntimeError(f"Failed to download video: {e}")
    
    # Find the downloaded file
    video_path = os.path.join(output_dir, 'video.mp4')
    if os.path.exists(video_path):
        return video_path, title, duration
    
    for ext in ['mp4', 'webm', 'mkv', 'avi']:
        p = os.path.join(output_dir, f'video.{ext}')
        if os.path.exists(p):
            return p, title, duration
    
    raise RuntimeError("Downloaded video file not found")


def get_video_info(video_path: str) -> dict:
    """Get video duration, fps, resolution."""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    info = json.loads(result.stdout)
    
    duration = 0
    fps = 0
    width = 0
    height = 0
    
    if 'format' in info:
        duration = float(info['format'].get('duration', 0))
    
    for stream in info.get('streams', []):
        if stream['codec_type'] == 'video':
            fps_str = stream.get('r_frame_rate', '0/1')
            if '/' in fps_str:
                num, den = fps_str.split('/')
                fps = float(num) / float(den) if den != '0' else 0
            width = stream.get('width', 0)
            height = stream.get('height', 0)
            break
    
    return {'duration': duration, 'fps': fps, 'width': width, 'height': height}


def extract_keyframes_scene_detect(video_path: str, output_dir: str, 
                                    min_scene_duration: float = 0.5,
                                    max_frames: int = 50,
                                    frame_width: int = 480) -> list:
    """
    Use FFmpeg scene detection to extract key frames.
    Uses adaptive thresholds: starts at 0.3, drops to 0.2 → 0.1 → 0.05
    if no scene changes detected.
    Returns list of {'time': seconds, 'file': 'filename.jpg'}.
    """
    frames_dir = os.path.join(output_dir, 'frames')
    os.makedirs(frames_dir, exist_ok=True)
    
    # Adaptive scene detection: try progressively lower thresholds
    thresholds = [0.3, 0.2, 0.1, 0.05]
    frames = []
    threshold_used = None
    
    for thresh in thresholds:
        print(f"Trying scene threshold: {thresh}...", file=sys.stderr)
        
        # Clean previous attempt
        for old_f in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, old_f))
        
        t0 = time.time()
        extract_cmd = [
            'ffmpeg', '-i', video_path,
            '-filter:v', f"select='gt(scene,{thresh})',scale={frame_width}:-1",
            '-vsync', 'vfr', '-q:v', '3',
            os.path.join(frames_dir, 'frame_%06d.jpg')
        ]
        subprocess.run(extract_cmd, capture_output=True, text=True, timeout=600)
        
        frames = sorted(
            [os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith('.jpg')]
        )
        
        elapsed = time.time() - t0
        print(f"  Found {len(frames)} frames in {elapsed:.1f}s", file=sys.stderr)
        
        if len(frames) >= 3:
            threshold_used = thresh
            break
    
    # Still no frames with scene detection? Try time-based fallback
    if not frames:
        print("No scene changes even at lowest threshold, using time-based extraction...", file=sys.stderr)
        return extract_keyframes_time_based(video_path, output_dir, frame_width, max_frames)
    
    # How many scenes naturally detected by FFmpeg?
    natural_scenes = len(frames)
    
    # Evenly sample only if naturally-detected scenes exceed the max limit
    if len(frames) > max_frames:
        step = len(frames) / max_frames
        frames = [frames[int(i * step)] for i in range(max_frames)]
        print(f"Sampled {len(frames)} frames from {natural_scenes} natural scenes (max={max_frames})", file=sys.stderr)
    else:
        print(f"Using all {natural_scenes} naturally detected scenes (threshold={threshold_used}, max={max_frames})", file=sys.stderr)
    
    # Get timestamps from video meta
    info = get_video_info(video_path)
    duration = info.get('duration', 60)
    
    # Estimate timestamps: frames are from scene detection (order preserved)
    result = []
    count = len(frames)
    for i, fp in enumerate(frames):
        result.append({
            'time': round(i * duration / max(count, 1), 1),
            'file': fp,
            'filename': os.path.basename(fp),
        })
    
    print(f"Extracted {len(result)} key frames", file=sys.stderr)
    return result


def extract_keyframes_time_based(video_path: str, output_dir: str,
                                  frame_width: int = 480,
                                  max_frames: int = 50) -> list:
    """Fallback: extract frames at regular intervals.
    
    For static-content videos (talking head, slides, screen recordings
    with no scene changes), extracts fewer frames at strategic positions
    to avoid wasting space on near-identical frames.
    """
    info = get_video_info(video_path)
    duration = info.get('duration', 60)
    
    if duration <= 0:
        duration = 60
    
    # For static-content videos (no scene changes), extract at strategic points
    # rather than evenly spaced — front-load frames near content transitions
    strategic_points = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9]
    
    if duration <= 60:  # < 1 min: 6 frames at strategic points
        time_points = [p * duration for p in strategic_points]
    elif duration <= 300:  # 1-5 min: 8 frames
        time_points = [p * duration for p in strategic_points]
        # Add 2 more mid-way
        time_points.insert(2, 0.15 * duration)
        time_points.append(0.8 * duration)
    else:  # > 5 min: 12 frames
        time_points = [i * duration / 12 for i in range(12)]
    
    # Cap at max_frames
    if len(time_points) > max_frames:
        time_points = time_points[:max_frames]
    
    frames_dir = os.path.join(output_dir, 'frames')
    os.makedirs(frames_dir, exist_ok=True)
    
    print(f"Time-based extraction: {len(time_points)} frames at strategic positions", file=sys.stderr)
    
    # Extract frames at specific timestamps using -ss
    frames = []
    for i, t in enumerate(time_points):
        output_path = os.path.join(frames_dir, f'frame_{i+1:06d}.jpg')
        cmd = [
            'ffmpeg', '-ss', str(t), '-i', video_path,
            '-vframes', '1',
            '-vf', f'scale={frame_width}:-1',
            '-q:v', '3',
            output_path
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if os.path.exists(output_path):
            frames.append({
                'time': round(t, 1),
                'file': output_path,
                'filename': f'frame_{i+1:06d}.jpg',
            })
    
    return frames


def create_contact_sheet(frames: list, output_dir: str, cols: int = 5) -> str:
    """
    Create a contact sheet (grid mosaic) of all key frames in a single image.
    Returns path to the contact sheet image.
    """
    if not frames:
        return None
    
    # Calculate grid dimensions
    total = len(frames)
    cols = min(cols, total)
    rows = (total + cols - 1) // cols
    
    # Build FFmpeg filter to tile frames into a grid
    frame_list_file = os.path.join(output_dir, 'frame_list.txt')
    
    # FFmpeg concat needs actual video streams. Instead, use ImageMagick if available,
    # or build a montage with ffmpeg
    # Simpler: write the frames list and use ffmpeg's hstack/vstack or tile
    
    # Actually, let's use a simpler approach: build a contact sheet with Python+PIL
    # Check if PIL is available
    try:
        from PIL import Image
        return _create_contact_sheet_pil(frames, output_dir, cols)
    except ImportError:
        return _create_contact_sheet_ffmpeg(frames, output_dir, cols)


def _create_contact_sheet_pil(frames: list, output_dir: str, cols: int) -> str:
    """Create contact sheet using Pillow."""
    from PIL import Image, ImageDraw, ImageFont
    
    # Load all images
    images = []
    for f in frames:
        try:
            img = Image.open(f['file'])
            images.append(img)
        except Exception as e:
            print(f"  Warning: skipping {f['filename']}: {e}", file=sys.stderr)
    
    if not images:
        return None
    
    # Use thumbnail width (they're already scaled by ffmpeg)
    thumb_w = images[0].width
    thumb_h = max(img.height for img in images)
    
    # Add padding
    pad = 4
    label_h = 20
    
    total_w = cols * (thumb_w + pad) + pad
    rows = (len(images) + cols - 1) // cols
    total_h = rows * (thumb_h + label_h + pad) + pad
    
    # Create canvas (dark background)
    canvas = Image.new('RGB', (total_w, total_h), (30, 30, 30))
    draw = ImageDraw.Draw(canvas)
    
    # Try to load font for timestamps
    font = None
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        try:
            font = ImageFont.load_default()
        except:
            pass
    
    for i, (img, frame_info) in enumerate(zip(images, frames)):
        x = pad + (i % cols) * (thumb_w + pad)
        y = pad + (i // cols) * (thumb_h + label_h + pad)
        
        # Paste thumbnail
        img_resized = img.resize((thumb_w, thumb_h), Image.LANCZOS)
        canvas.paste(img_resized, (x, y))
        
        # Draw timestamp label
        ts = _format_ts(frame_info.get('time', 0))
        label = f"[{ts}]"
        if font:
            # Draw text shadow
            draw.text((x + 3, y + thumb_h + 2), label, fill=(180, 180, 180), font=font)
        else:
            draw.text((x + 2, y + thumb_h + 2), label, fill=(180, 180, 180))
    
    output_path = os.path.join(output_dir, 'contact_sheet.jpg')
    canvas.save(output_path, 'JPEG', quality=85)
    
    print(f"Contact sheet saved: {output_path} ({total_w}x{total_h}, {len(images)} frames)", file=sys.stderr)
    return output_path


def _create_contact_sheet_ffmpeg(frames: list, output_dir: str, cols: int) -> str:
    """Create contact sheet using FFmpeg tile filter (no PIL needed)."""
    if not frames:
        return None
    
    # FFmpeg's tile filter approach requires building a filter graph
    # Since frames are already scaled, use the tile filter
    frames_dir = os.path.join(output_dir, 'frames')
    total = len(frames)
    rows = (total + cols - 1) // cols
    
    # Use ffmpeg's tile filter with pattern matching
    # Input all frames as individual streams
    input_args = []
    for f in frames:
        input_args.extend(['-i', f['file']])
    
    # Build filter complex to tile them
    filter_parts = []
    for i in range(total):
        filter_parts.append(f"[{i}:v]")
    
    filter_str = ''.join(filter_parts) + f"hstack=inputs={min(total, cols)}"
    
    # For multiple rows, need to do this differently
    # Simpler approach: use individual montage via overlay if total <= cols
    if total <= cols:
        cmd = input_args + [
            '-filter_complex', filter_str,
            '-frames:v', '1',
            os.path.join(output_dir, 'contact_sheet.jpg')
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=60)
            return os.path.join(output_dir, 'contact_sheet.jpg')
        except:
            return None
    else:
        # Multiple rows - build row by row
        # This is complex with ffmpeg, just skip contact sheet in this case
        print("  Note: Grid too large for FFmpeg-only contact sheet (no PIL)", file=sys.stderr)
        return None


def _format_ts(seconds: float) -> str:
    seconds = max(0, seconds)
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def calc_total_size(frames: list) -> int:
    """Calculate total disk size of all frame files in bytes."""
    total = 0
    for f in frames:
        try:
            total += os.path.getsize(f['file'])
        except:
            pass
    return total


def auto_max_frames(duration: float) -> int:
    """Auto-calculate frame count from video duration.
    
    - < 1 min: 10 frames
    - 1-3 min: 15 frames
    - 3-5 min: 20 frames
    - 5-15 min: 30 frames
    - > 15 min: 30 frames (cap)
    """
    if duration <= 0:
        return 20
    if duration < 60:  # < 1 min
        return 10
    if duration < 180:  # 1-3 min
        return 15
    if duration < 300:  # 3-5 min
        return 20
    if duration < 900:  # 5-15 min
        return 30
    return 30  # > 15 min


def save_manifest(frames: list, output_dir: str, video_title: str, duration: float):
    """Save frame manifest as JSON."""
    total_size = calc_total_size(frames)
    manifest = {
        'title': video_title,
        'duration': duration,
        'total_frames': len(frames),
        'total_size_bytes': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'frames': [
            {
                'time': f['time'],
                'time_str': _format_ts(f['time']),
                'file': f['file'],
                'filename': f['filename'],
            }
            for f in frames
        ]
    }
    
    manifest_path = os.path.join(output_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"Manifest saved: {manifest_path}", file=sys.stderr)
    return manifest_path


def main():
    parser = argparse.ArgumentParser(
        description='Extract key frames from video for AI visual analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output structure:
  <output-dir>/
    contact_sheet.jpg   # All key frames in a grid (single image)
    manifest.json       # Frame list with timestamps
    frames/             # Individual key frames (jpg)
    
Usage:
  python video_vision.py https://www.youtube.com/watch?v=xxx -o ./frames
  python video_vision.py BV12ZDuBwEhX --no-grid --max-frames 20
        """)
    
    parser.add_argument('input', help='Video URL or ID')
    parser.add_argument('--output-dir', '-o', help='Output directory (default: temp dir)')
    parser.add_argument('--no-grid', action='store_true', 
                        help='Save individual frames only, no contact sheet')
    parser.add_argument('--max-frames', type=int, default=0,
                        help='Maximum key frames to extract (default: auto-calculate from duration)')
    parser.add_argument('--frame-width', type=int, default=480,
                        help='Frame width in pixels (default: 480)')
    parser.add_argument('--grid-cols', type=int, default=5,
                        help='Number of columns in contact sheet (default: 5)')
    
    args = parser.parse_args()
    
    platform = detect_platform(args.input)
    clean_output = False
    
    # Setup output directory
    if args.output_dir:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = tempfile.mkdtemp(prefix='video_frames_')
        clean_output = True
    
    tmpdir = tempfile.mkdtemp(prefix='video_dl_')
    
    try:
        # Step 1: Download video (low res)
        video_path, title, duration = download_video(args.input, tmpdir, platform)
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"Video downloaded: {video_path} ({file_size_mb:.1f}MB)", file=sys.stderr)
        
        # Auto-calculate max-frames if default (0)
        if args.max_frames <= 0:
            args.max_frames = auto_max_frames(duration)
            print(f"Auto frame count: {args.max_frames} (from {duration}s video)", file=sys.stderr)
        
        # Step 2: Extract key frames
        frames = extract_keyframes_scene_detect(
            video_path, output_dir,
            max_frames=args.max_frames,
            frame_width=args.frame_width
        )
        
        if not frames:
            print("Error: No frames extracted.", file=sys.stderr)
            sys.exit(1)
        
        print(f"Extracted {len(frames)} key frames", file=sys.stderr)
        
        # Step 3: Create contact sheet
        contact_sheet = None
        if not args.no_grid:
            contact_sheet = create_contact_sheet(frames, output_dir, args.grid_cols)
            if contact_sheet:
                print(f"Contact sheet: {contact_sheet}", file=sys.stderr)
        
        # Step 4: Save manifest
        manifest_path = save_manifest(frames, output_dir, title, duration)
        
        # Step 5: Output summary to stdout
        print(f"\n[VISUAL ANALYSIS READY]", file=sys.stderr)
        print(f"Title: {title}", file=sys.stderr)
        print(f"Duration: {duration}s", file=sys.stderr)
        print(f"Key frames: {len(frames)}", file=sys.stderr)
        print(f"Output directory: {output_dir}", file=sys.stderr)
        if contact_sheet:
            print(f"Contact sheet: {contact_sheet}", file=sys.stderr)
        print(f"Manifest: {manifest_path}", file=sys.stderr)
        print(f"\nTip: Use --vision flag in video_subtitle.py instead of running this directly.", file=sys.stderr)
        
        total_size = calc_total_size(frames)
        
        # Print frame info to stdout for piping
        print("---")
        print(json.dumps({
            'output_dir': output_dir,
            'contact_sheet': contact_sheet,
            'manifest': manifest_path,
            'total_frames': len(frames),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'title': title,
            'duration': duration,
            'frames': [{'time': f['time'], 'file': f['file']} for f in frames],
        }, ensure_ascii=False))
        
    except Exception as e:
        import traceback
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Video Audio Transcriber — download audio and transcribe with Whisper.
Used as fallback when videos have no subtitles/captions.
Supports YouTube, Bilibili, and direct video URLs.

Usage:
    python video_asr.py <URL_or_ID> [--output FILE] [--model MODEL] [--lang LANG]
Examples:
    python video_asr.py https://www.youtube.com/watch?v=xxx
    python video_asr.py https://www.bilibili.com/video/BVxxx
    python video_asr.py https://example.com/video.mp4 --lang zh --model medium
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time


def format_timestamp(seconds: float) -> str:
    seconds = max(0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{m:02d}:{s:02d},{ms:03d}"


def download_audio(url: str, output_dir: str) -> str:
    """Download audio from video URL using yt-dlp. Returns path to audio file."""
    print(f"Downloading audio from: {url}", file=sys.stderr)

    output_template = os.path.join(output_dir, 'audio.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'progress_hooks': [],
        'logger': None,
    }

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise RuntimeError(f"Failed to download audio: {e}")

    # Find the downloaded file
    audio_path = os.path.join(output_dir, 'audio.wav')
    if os.path.exists(audio_path):
        return audio_path

    # Try other extensions
    for ext in ['mp3', 'm4a', 'opus', 'webm', 'wav']:
        p = os.path.join(output_dir, f'audio.{ext}')
        if os.path.exists(p):
            return p

    raise RuntimeError("Downloaded audio file not found")


def transcribe(audio_path: str, model_size: str = 'base', language: str = None) -> list:
    """
    Transcribe audio file using faster-whisper.
    Returns list of {start, end, content} dicts.
    """
    from faster_whisper import WhisperModel

    print(f"Loading Whisper model: {model_size} (first run will download ~75MB-1.5GB)...", file=sys.stderr)

    # Use int8 for speed, fall back to float32 if no CUDA
    try:
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    except Exception:
        print("int8 not supported, using float32", file=sys.stderr)
        model = WhisperModel(model_size, device="cpu", compute_type="float32")

    print(f"Transcribing: {os.path.basename(audio_path)}", file=sys.stderr)
    start_time = time.time()

    segments_iter, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        vad_filter=True,  # Skip silent parts
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})", file=sys.stderr)

    entries = []
    for segment in segments_iter:
        entries.append({
            'start': round(segment.start, 1),
            'end': round(segment.end, 1),
            'content': segment.text.strip(),
        })

    elapsed = time.time() - start_time
    print(f"Transcription done: {len(entries)} segments in {elapsed:.1f}s", file=sys.stderr)

    return entries


def format_output(entries: list, fmt: str) -> str:
    """Format entries to desired output format."""
    if fmt == 'srt':
        lines = []
        for i, e in enumerate(entries, 1):
            lines.append(str(i))
            lines.append(f"{format_timestamp(e['start'])} --> {format_timestamp(e['end'])}")
            lines.append(e['content'])
            lines.append('')
        return '\n'.join(lines)
    elif fmt == 'vtt':
        lines = ['WEBVTT', '']
        for e in entries:
            ts = lambda s: format_timestamp(s).replace(',', '.')
            lines.append(f"{ts(e['start'])} --> {ts(e['end'])}")
            lines.append(e['content'])
            lines.append('')
        return '\n'.join(lines)
    elif fmt == 'json':
        return json.dumps(entries, ensure_ascii=False, indent=2)
    elif fmt == 'text-only':
        return '\n'.join(e['content'] for e in entries)
    else:
        # default: plain text with timestamps
        lines = []
        for e in entries:
            s = format_timestamp(e['start'])
            en = format_timestamp(e['end'])
            lines.append(f"[{s} --> {en}] {e['content']}")
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Download video audio and transcribe with Whisper ASR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Models (size vs accuracy vs speed):
  tiny      ~75MB   Fastest, least accurate
  base      ~150MB  Good for short/clear audio
  small     ~500MB  Better accuracy
  medium    ~1.5GB  Good balance (recommended)
  large-v3  ~3GB    Most accurate, slowest

Examples:
  python video_asr.py https://www.youtube.com/watch?v=xxx
  python video_asr.py https://www.bilibili.com/video/BVxxx -o result.txt
  python video_asr.py https://youtu.be/xxx --lang zh --model medium -f srt
        """)

    parser.add_argument('input', help='Video URL or ID (YouTube, Bilibili, or direct video URL)')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--format', '-f', default='default',
                        choices=['default', 'srt', 'vtt', 'json', 'text-only'],
                        help='Output format (default: plain text with timestamps)')
    parser.add_argument('--model', '-m', default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large-v3', 'large-v2', 'large'],
                        help='Whisper model size (default: base)')
    parser.add_argument('--lang', '-l', default=None,
                        help='Language code for transcription (e.g. zh, en, ja). Auto-detect if not set.')

    args = parser.parse_args()

    tmpdir = tempfile.mkdtemp(prefix='video_asr_')
    audio_path = None

    try:
        # Step 1: Download audio
        audio_path = download_audio(args.input, tmpdir)
        file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"Audio downloaded: {audio_path} ({file_size_mb:.1f}MB)", file=sys.stderr)

        # Step 2: Transcribe
        entries = transcribe(audio_path, model_size=args.model, language=args.lang)

        if not entries:
            print("Warning: No speech detected in audio.", file=sys.stderr)
            sys.exit(0)

        # Step 3: Format and output
        text = format_output(entries, args.format)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved to {args.output}", file=sys.stderr)
        else:
            print(text)

    except Exception as e:
        import traceback
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    finally:
        # Cleanup temp files
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass
        try:
            os.rmdir(tmpdir)
        except:
            pass


if __name__ == '__main__':
    main()

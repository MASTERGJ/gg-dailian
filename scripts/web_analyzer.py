#!/usr/bin/env python3
"""
Web Page Analyzer — extract text and screenshots from web pages.
Outputs the same entry format as video_subtitle.py for unified classification.

Usage:
    python web_analyzer.py <URL> [--screenshot]
    python web_analyzer.py <URL> --screenshot --screenshot-dir ./shots

Output modes:
  text-only   Just extracted text (no timestamps)
  json        Full JSON entries
  default     Text with paragraph markers

Each entry = one paragraph or section of the page.
"""

import argparse
import json
import os
import re
import sys
import tempfile
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser


# ============================================================
# HTML Text Extractor
# ============================================================

class TextExtractor(HTMLParser):
    """Extract readable text from HTML, preserving paragraph breaks."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.current_text = []
        self.skip_tags = {'script', 'style', 'noscript', 'svg', 'path'}
        self.skip_depth = 0
        self.in_skip = False
        self.block_tags = {
            'p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'section', 'article', 'blockquote', 'pre', 'td', 'th',
        }
        self.last_was_block = True

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self.skip_tags:
            self.skip_depth += 1
            self.in_skip = True
        if tag in self.block_tags and not self.in_skip:
            self._flush_text()

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.skip_tags:
            self.skip_depth -= 1
            if self.skip_depth <= 0:
                self.skip_depth = 0
                self.in_skip = False
        if tag in self.block_tags and not self.in_skip:
            self._flush_text()

    def handle_data(self, data):
        if not self.in_skip:
            text = data.strip()
            if text:
                self.current_text.append(text)

    def _flush_text(self):
        if self.current_text:
            line = ' '.join(self.current_text).strip()
            if line:
                self.result.append(line)
            self.current_text = []

    def get_text(self) -> str:
        self._flush_text()
        return '\n'.join(self.result)


def fetch_page(url: str, timeout: int = 15) -> str:
    """Fetch HTML from a URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    return html


def html_to_entries(html: str, url: str) -> list:
    """Convert HTML to entry list [{start: index, end: index+1, content: text}]."""
    extractor = TextExtractor()
    extractor.feed(html)
    paragraphs = extractor.get_text().split('\n')

    # Filter empty/minimal paragraphs
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 15]

    entries = []
    for i, p in enumerate(paragraphs):
        entries.append({
            'start': float(i),
            'end': float(i + 1),
            'content': p,
        })

    return entries


# ============================================================
# Screenshot (via agent-browser)
# ============================================================

def take_screenshot(url: str, output_dir: str) -> str:
    """Take a screenshot of the web page using agent-browser."""
    screenshot_path = os.path.join(output_dir, 'web_screenshot.png')

    try:
        cmd = [
            'agent-browser', 'goto', url,
            '--timeout', '10000',
        ]
        import subprocess
        subprocess.run(cmd, capture_output=True, text=True, timeout=15)

        # Take screenshot
        cmd2 = [
            'agent-browser', 'screenshot',
            '--path', screenshot_path,
        ]
        subprocess.run(cmd2, capture_output=True, text=True, timeout=15)

        if os.path.exists(screenshot_path):
            size_kb = os.path.getsize(screenshot_path) / 1024
            print(f"Screenshot taken: {screenshot_path} ({size_kb:.0f}KB)", file=sys.stderr)
            return screenshot_path
    except Exception as e:
        print(f"Screenshot failed: {e}", file=sys.stderr)
        print("Tip: Install agent-browser or use --no-screenshot", file=sys.stderr)

    return None


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Extract text and screenshots from web pages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python web_analyzer.py https://example.com
  python web_analyzer.py https://example.com --screenshot
  python web_analyzer.py https://example.com -f text-only
        """)

    parser.add_argument('url', help='Web page URL')
    parser.add_argument('--screenshot', '-s', action='store_true',
                        help='Also take a screenshot of the page (requires agent-browser)')
    parser.add_argument('--screenshot-dir', type=str, default='',
                        help='Output directory for screenshot (default: auto temp)')
    parser.add_argument('--format', '-f', default='default',
                        choices=['default', 'json', 'text-only'],
                        help='Output format (default: text with section markers)')
    parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    url = args.url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    tmpdir = tempfile.mkdtemp(prefix='web_analyze_')

    try:
        # Step 1: Fetch and extract text
        print(f"Fetching: {url}", file=sys.stderr)
        html = fetch_page(url)
        entries = html_to_entries(html, url)
        print(f"Extracted {len(entries)} paragraphs", file=sys.stderr)

        if not entries:
            print("Warning: No meaningful text found on page.", file=sys.stderr)

        # Step 2: Screenshot (optional)
        screenshot_path = None
        if args.screenshot:
            screenshot_path = take_screenshot(url, tmpdir if not args.screenshot_dir else args.screenshot_dir)

        # Step 3: Output
        if args.format == 'text-only':
            text = '\n'.join(e['content'] for e in entries)
        elif args.format == 'json':
            formatted = [{'section': i + 1, 'content': e['content']} for i, e in enumerate(entries)]
            text = json.dumps(formatted, ensure_ascii=False, indent=2)
        else:
            lines = []
            for i, e in enumerate(entries):
                lines.append(f"[Section {i + 1}]")
                lines.append(e['content'])
                lines.append('')
            text = '\n'.join(lines)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved to {args.output}", file=sys.stderr)
        else:
            if screenshot_path:
                print(f"\n# Screenshot: {screenshot_path}", file=sys.stderr)
                print(f"# Size: {os.path.getsize(screenshot_path) / 1024:.0f}KB\n", file=sys.stderr)
            print(text)

    except Exception as e:
        import traceback
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    finally:
        # Cleanup temp
        try:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass


if __name__ == '__main__':
    main()

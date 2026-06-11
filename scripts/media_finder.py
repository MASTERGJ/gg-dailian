#!/usr/bin/env python3
"""
Find downloadable media URLs from a web page.

This is a lightweight fallback for sites that are not supported by yt-dlp.
It scans page HTML and embedded JSON for direct MP4/WebM/M3U8 URLs.
"""

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request


MEDIA_RE = re.compile(
    r"""(?P<url>(?:https?:)?//[^"'<>\s\\]+?\.(?:mp4|webm|m3u8)(?:\?[^"'<>\s\\]*)?)""",
    re.IGNORECASE,
)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


def normalize_url(url: str, page_url: str) -> str:
    url = html.unescape(url).replace("\\/", "/")
    if url.startswith("//"):
        return "https:" + url
    return urllib.parse.urljoin(page_url, url)


def find_media_urls(page_url: str, text: str) -> list[dict]:
    seen = set()
    results = []
    for match in MEDIA_RE.finditer(text):
        # Avoid false positives from thumbnail names such as
        # video.mp4-000002.jpg; those are images, not media streams.
        if match.end() < len(text) and text[match.end()] == "-":
            continue
        media_url = normalize_url(match.group("url"), page_url)
        if media_url in seen:
            continue
        seen.add(media_url)
        lower = media_url.lower()
        if ".m3u8" in lower:
            kind = "hls"
        elif ".webm" in lower:
            kind = "webm"
        else:
            kind = "mp4"
        results.append({"type": kind, "url": media_url})
    return results


def extract_title(text: str) -> str:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if not title_match:
        return ""
    title = re.sub(r"\s+", " ", title_match.group(1)).strip()
    return html.unescape(title)


def main() -> int:
    parser = argparse.ArgumentParser(description="Find media URLs from a web page")
    parser.add_argument("url", help="Page URL")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    try:
        text = fetch_text(args.url)
    except Exception as exc:
        print(f"Fetch failed: {exc}", file=sys.stderr)
        return 1

    title = extract_title(text)
    media = find_media_urls(args.url, text)
    output = {"url": args.url, "title": title, "media": media}

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if title:
            print(f"Title: {title}")
        print(f"Found media: {len(media)}")
        for idx, item in enumerate(media, 1):
            print(f"{idx}. [{item['type']}] {item['url']}")

    return 0 if media else 2


if __name__ == "__main__":
    raise SystemExit(main())

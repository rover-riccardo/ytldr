# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "youtube-transcript-api",
#     "yt-dlp",
# ]
# ///

import sys
import re
import argparse
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL


def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    sys.exit(f"Could not extract video ID from: {url}")


def fetch_metadata(url: str) -> dict:
    with YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "title": info.get("title", "Untitled"),
        "description": info.get("description", ""),
        "channel": info.get("channel", ""),
        "upload_date": info.get("upload_date", ""),
    }


def format_timestamp(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"


def fetch_transcript(video_id: str, interval: int = 30) -> str:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    snippets = transcript.snippets
    if not snippets:
        return ""
    paragraphs: list[str] = []
    current_words: list[str] = []
    chunk_start = 0.0
    next_break = interval
    for snippet in snippets:
        if snippet.start >= next_break and current_words:
            paragraphs.append(f"**[{format_timestamp(chunk_start)}]** " + " ".join(current_words))
            current_words = []
            chunk_start = snippet.start
            next_break = chunk_start + interval
        current_words.append(snippet.text)
    if current_words:
        paragraphs.append(f"**[{format_timestamp(chunk_start)}]** " + " ".join(current_words))
    return "\n\n".join(paragraphs)


def slugify(text: str) -> str:
    return re.sub(r"[^\w\s-]", "", text).strip().replace(" ", "-").lower()[:80]


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--save", action="store_true", help="Save output to a markdown file")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)

    print(f"Fetching metadata for {video_id}...", file=sys.stderr)
    meta = fetch_metadata(args.url)

    print("Fetching transcript...", file=sys.stderr)
    transcript = fetch_transcript(video_id)

    date = meta["upload_date"]
    date_fmt = f"{date[:4]}-{date[4:6]}-{date[6:]}" if len(date) == 8 else date

    md = f"""# {meta['title']}

- **Channel:** {meta['channel']}
- **Date:** {date_fmt}
- **URL:** {args.url}

## Description

{meta['description']}

## Transcript

{transcript}
"""

    if args.save:
        filename = f"{slugify(meta['title'])}.md"
        Path(filename).write_text(md)
        print(f"Saved to {filename}", file=sys.stderr)
    else:
        print(md)


if __name__ == "__main__":
    main()

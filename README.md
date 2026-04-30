# ytldr

Fetch YouTube video transcripts as readable markdown with timestamps.

## Install

Requires [uv](https://docs.astral.sh/uv/) and [claude](https://docs.anthropic.com/en/docs/claude-code) (for `--summary`).

```bash
uv tool install .
```

This makes `ytldr` available globally.

## Usage

```bash
# Print transcript to stdout
ytldr "https://www.youtube.com/watch?v=VIDEO_ID"

# Save to a markdown file
ytldr "https://www.youtube.com/watch?v=VIDEO_ID" --save

# Summarize with Claude Haiku (default 6 bullet points)
ytldr "https://www.youtube.com/watch?v=VIDEO_ID" --summary

# Summarize with 3 bullet points
ytldr "https://www.youtube.com/watch?v=VIDEO_ID" --summary 3

# Combine: summarize and save
ytldr "https://www.youtube.com/watch?v=VIDEO_ID" --summary --save
```

## Custom summary prompt

Edit `prompt.txt` to change how summaries are generated. Use `{N}` as a placeholder for the number of bullet points. If the file is missing, a built-in default is used.

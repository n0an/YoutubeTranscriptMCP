# YouTube MCP Server

A simple Model Context Protocol (MCP) server that provides tools to extract YouTube video IDs and fetch transcripts.

## Installation

### Using uv (recommended)
```bash
uv add "mcp[cli]" youtube-transcript-api
```

### Using pip
```bash
pip install -r requirements.txt
```

## Usage

### Development Mode
Test the server with MCP Inspector:
```bash
uv run mcp dev youtube_mcp_server.py
```

### Claude Desktop Integration
Install in Claude Desktop:
```bash
uv run mcp install youtube_mcp_server.py --name "YouTube Tools"
```

### Direct Execution
```bash
python youtube_mcp_server.py
```

## Available Tools

1. **get_youtube_video_id(url)**: Extract video ID from YouTube URLs
2. **get_youtube_transcript(video_url_or_id, language="en")**: Get full transcript with timestamps

## Example Usage

The tools can extract video IDs from various YouTube URL formats:
- `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- `https://youtu.be/dQw4w9WgXcQ`
- `dQw4w9WgXcQ` (direct video ID)

Transcripts are returned with timestamps in `[MM:SS] text` format.

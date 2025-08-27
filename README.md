# YouTube & Web Search MCP Server

A Model Context Protocol (MCP) server that provides tools to extract YouTube video IDs, fetch transcripts, and search the web using Tavily API.

## Installation

### Using uv (recommended)
```bash
# Install all dependencies from pyproject.toml
uv sync

# Or install specific packages (if starting fresh)
uv add "mcp[cli]" youtube-transcript-api tavily-python
```

## Usage

### Run server
```bash
uv run youtube_mcp_server.py
```

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

## Environment Variables

For web search functionality, you need to set your Tavily API key:
```bash
export TAVILY_API_KEY="your_tavily_api_key_here"
```

Get your free API key at: https://tavily.com

## Available Tools

1. **get_youtube_video_id(url)**: Extract video ID from YouTube URLs
2. **get_youtube_transcript(video_url_or_id, language="en")**: Get full transcript with timestamps
3. **search_web(query, max_results=5, include_domains=None, exclude_domains=None)**: Search the web using Tavily API

## Example Usage

### YouTube Tools
The tools can extract video IDs from various YouTube URL formats:
- `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- `https://youtu.be/dQw4w9WgXcQ`
- `dQw4w9WgXcQ` (direct video ID)

Transcripts are returned with timestamps in `[MM:SS] text` format.

### Web Search
The web search tool provides comprehensive search results with quick answers:
- Basic search: `search_web("artificial intelligence trends 2024")`
- Limited results: `search_web("python tutorials", max_results=3)`
- Domain filtering: `search_web("machine learning", include_domains=["wikipedia.org", "arxiv.org"])`

Results include titles, URLs, content snippets, and often a quick answer summary.

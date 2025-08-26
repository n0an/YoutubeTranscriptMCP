"""
YouTube MCP Server - Extract video IDs and transcripts from YouTube videos.

Run with:
    uv run mcp dev youtube_mcp_server.py
    or
    python youtube_mcp_server.py
"""

import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable

from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("YouTube Tools Server")


@mcp.tool()
def get_youtube_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - And other common formats
    """
    # YouTube URL patterns
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If no pattern matches, check if it's already a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url.strip()):
        return url.strip()
    
    raise ValueError(f"Could not extract video ID from URL: {url}")


@mcp.tool()
def get_youtube_transcript(video_url_or_id: str, language: str = "en") -> str:
    """
    Get the full transcript of a YouTube video.
    
    Args:
        video_url_or_id: YouTube URL or video ID
        language: Language code for transcript (default: "en")
    
    Returns:
        Full transcript as formatted text
    """
    try:
        # Extract video ID if URL is provided
        video_id = get_youtube_video_id(video_url_or_id)
        
        # Create API instance and get transcript
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=[language])
        
        # Get raw transcript data
        transcript_data = transcript.to_raw_data()
        
        # Format transcript
        formatted_transcript = ""
        for entry in transcript_data:
            timestamp = entry['start']
            text = entry['text']
            
            # Convert timestamp to minutes:seconds format
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            
            formatted_transcript += f"[{time_str}] {text}\n"
        
        return formatted_transcript.strip()
        
    except NoTranscriptFound:
        try:
            api = YouTubeTranscriptApi()
            available_transcripts = api.list(video_id)
            available_languages = [t.language_code for t in available_transcripts]
            return f"No transcript found for language '{language}'. Available languages: {available_languages}"
        except:
            return f"No transcript found for language '{language}' and could not retrieve available languages."
    
    except VideoUnavailable:
        return f"Video {video_id} is unavailable or doesn't exist."
    
    except Exception as e:
        return f"Error getting transcript: {str(e)}"


def main():
    """Run the YouTube MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()

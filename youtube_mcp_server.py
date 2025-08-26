"""
YouTube MCP Server - Extract video IDs and transcripts from YouTube videos, and search the web.

Run with:
    uv run mcp dev youtube_mcp_server.py
    or
    python youtube_mcp_server.py
"""

import os
import re
from typing import Optional, List, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable
from tavily import TavilyClient

from mcp.server.fastmcp import FastMCP

# Create the MCP server
# mcp = FastMCP("YouTube & Web Search Tools Server", host="0.0.0.0", port=8000)
mcp = FastMCP("YouTube & Web Search Tools Server")



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


@mcp.tool()
def search_web(query: str, max_results: int = 5, include_domains: Optional[List[str]] = None, exclude_domains: Optional[List[str]] = None) -> str:
    """
    Search the web using Tavily API to get comprehensive information about any topic.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5, max: 20)
        include_domains: Optional list of domains to include in search (e.g., ["wikipedia.org", "github.com"])
        exclude_domains: Optional list of domains to exclude from search (e.g., ["example.com"])
    
    Returns:
        Formatted search results with titles, URLs, and content snippets
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY environment variable not set. Please set your Tavily API key."
        
        # Initialize Tavily client
        client = TavilyClient(api_key=api_key)
        
        # Prepare search parameters
        search_params = {
            "query": query,
            "max_results": min(max_results, 20),  # Cap at 20 as per Tavily limits
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": False
        }
        
        # Add domain filters if provided
        if include_domains:
            search_params["include_domains"] = include_domains
        if exclude_domains:
            search_params["exclude_domains"] = exclude_domains
        
        # Perform search
        response = client.search(**search_params)
        
        # Format results
        formatted_results = f"**Search Query:** {query}\n\n"
        
        # Add answer if available
        if response.get("answer"):
            formatted_results += f"**Quick Answer:**\n{response['answer']}\n\n"
        
        # Add search results
        if response.get("results"):
            formatted_results += "**Search Results:**\n\n"
            
            for i, result in enumerate(response["results"], 1):
                title = result.get("title", "No title")
                url = result.get("url", "No URL")
                content = result.get("content", "No content available")
                
                # Truncate content if too long
                if len(content) > 300:
                    content = content[:297] + "..."
                
                formatted_results += f"{i}. **{title}**\n"
                formatted_results += f"   URL: {url}\n"
                formatted_results += f"   {content}\n\n"
        else:
            formatted_results += "No search results found.\n"
        
        return formatted_results.strip()
        
    except Exception as e:
        return f"Error performing web search: {str(e)}"


def main():
    """Run the YouTube MCP server."""
    # mcp.run(transport="sse")
    mcp.run()


if __name__ == "__main__":
    main()

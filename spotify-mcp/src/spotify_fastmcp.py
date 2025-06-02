import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import json
import logging
from typing import List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from spotipy import SpotifyException

# import spotify_api
# from utils import normalize_redirect_uri
from . import spotify_api
from .utils import normalize_redirect_uri



def setup_logger():
    class Logger:
        def info(self, message):
            print(f"[INFO] {message}", file=sys.stderr)

        def error(self, message):
            print(f"[ERROR] {message}", file=sys.stderr)

    return Logger()


logger = setup_logger()

# Normalize the redirect URI to meet Spotify's requirements
if spotify_api.REDIRECT_URI:
    spotify_api.REDIRECT_URI = normalize_redirect_uri(spotify_api.REDIRECT_URI)

spotify_client = spotify_api.Client(logger)

# Initialize FastMCP
mcp = FastMCP("Spotify MCP")


# Pydantic models for tool inputs
class PlaybackAction(BaseModel):
    """Manages the current playback with the following actions:
    - get: Get information about user's current track.
    - start: Starts playing new item or resumes current playback if called with no uri.
    - pause: Pauses current playback.
    - skip: Skips current track.
    """
    action: str = Field(description="Action to perform: 'get', 'start', 'pause' or 'skip'.")
    spotify_uri: Optional[str] = Field(default=None, description="Spotify uri of item to play for 'start' action. If omitted, resumes current playback.")
    num_skips: Optional[int] = Field(default=1, description="Number of tracks to skip for `skip` action.")


class QueueAction(BaseModel):
    """Manage the playback queue - get the queue or add tracks."""
    action: str = Field(description="Action to perform: 'add' or 'get'.")
    track_id: Optional[str] = Field(default=None, description="Track ID to add to queue (required for add action)")


class SearchQuery(BaseModel):
    """Search for tracks, albums, artists, or playlists on Spotify."""
    query: str = Field(description="query term")
    qtype: Optional[str] = Field(default="track", description="Type of items to search for (track, album, artist, playlist, or comma-separated combination)")
    limit: Optional[int] = Field(default=10, description="Maximum number of items to return")


class GetInfoQuery(BaseModel):
    """Get detailed information about a Spotify item (track, album, artist, or playlist)."""
    item_uri: str = Field(description="URI of the item to get information about. If 'playlist' or 'album', returns its tracks. If 'artist', returns albums and top tracks.")


class PlaylistAction(BaseModel):
    """Manage Spotify playlists.
    - get: Get a list of user's playlists.
    - get_tracks: Get tracks in a specific playlist.
    - add_tracks: Add tracks to a specific playlist.
    - remove_tracks: Remove tracks from a specific playlist.
    - change_details: Change details of a specific playlist.
    """
    action: str = Field(description="Action to perform: 'get', 'get_tracks', 'add_tracks', 'remove_tracks', 'change_details'.")
    playlist_id: Optional[str] = Field(default=None, description="ID of the playlist to manage.")
    track_ids: Optional[List[str]] = Field(default=None, description="List of track IDs to add/remove.")
    name: Optional[str] = Field(default=None, description="New name for the playlist.")
    description: Optional[str] = Field(default=None, description="New description for the playlist.")


# Tool implementations
@mcp.tool()
def SpotifyPlayback(args: PlaybackAction) -> str:
    """Manages the current playback with various actions."""
    logger.info(f"Playback tool called with action: {args.action}")
    
    try:
        match args.action:
            case "get":
                logger.info("Attempting to get current track")
                curr_track = spotify_client.get_current_track()
                if curr_track:
                    logger.info(f"Current track retrieved: {curr_track.get('name', 'Unknown')}")
                    return json.dumps(curr_track, indent=2)
                logger.info("No track currently playing")
                return "No track playing."
                
            case "start":
                logger.info(f"Starting playback with uri: {args.spotify_uri}")
                spotify_client.start_playback(spotify_uri=args.spotify_uri)
                logger.info("Playback started successfully")
                return "Playback starting."
                
            case "pause":
                logger.info("Attempting to pause playback")
                spotify_client.pause_playback()
                logger.info("Playback paused successfully")
                return "Playback paused."
                
            case "skip":
                num_skips = args.num_skips or 1
                logger.info(f"Skipping {num_skips} tracks.")
                spotify_client.skip_track(n=num_skips)
                return "Skipped to next track."
                
            case _:
                return f"Unknown action: {args.action}"
                
    except SpotifyException as se:
        error_msg = f"Spotify Client error occurred: {str(se)}"
        logger.error(error_msg)
        return f"An error occurred with the Spotify Client: {str(se)}"
    except Exception as e:
        error_msg = f"Unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
def SpotifySearch(args: SearchQuery) -> str:
    """Search for tracks, albums, artists, or playlists on Spotify."""
    logger.info(f"Search tool called with query: {args.query}")
    
    try:
        search_results = spotify_client.search(
            query=args.query,
            qtype=args.qtype or "track",
            limit=args.limit or 10
        )
        logger.info("Search completed successfully.")
        return json.dumps(search_results, indent=2)
        
    except SpotifyException as se:
        error_msg = f"Spotify Client error occurred: {str(se)}"
        logger.error(error_msg)
        return f"An error occurred with the Spotify Client: {str(se)}"
    except Exception as e:
        error_msg = f"Unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
def SpotifyQueue(args: QueueAction) -> str:
    """Manage the playback queue - get the queue or add tracks."""
    logger.info(f"Queue tool called with action: {args.action}")
    
    try:
        match args.action:
            case "add":
                if not args.track_id:
                    logger.error("track_id is required for add to queue.")
                    return "track_id is required for add action"
                spotify_client.add_to_queue(args.track_id)
                return "Track added to queue."
                
            case "get":
                queue = spotify_client.get_queue()
                return json.dumps(queue, indent=2)
                
            case _:
                return f"Unknown queue action: {args.action}. Supported actions are: add and get."
                
    except SpotifyException as se:
        error_msg = f"Spotify Client error occurred: {str(se)}"
        logger.error(error_msg)
        return f"An error occurred with the Spotify Client: {str(se)}"
    except Exception as e:
        error_msg = f"Unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
def SpotifyGetInfo(args: GetInfoQuery) -> str:
    """Get detailed information about a Spotify item (track, album, artist, or playlist)."""
    logger.info(f"GetInfo tool called with uri: {args.item_uri}")
    
    try:
        item_info = spotify_client.get_info(item_uri=args.item_uri)
        return json.dumps(item_info, indent=2)
        
    except SpotifyException as se:
        error_msg = f"Spotify Client error occurred: {str(se)}"
        logger.error(error_msg)
        return f"An error occurred with the Spotify Client: {str(se)}"
    except Exception as e:
        error_msg = f"Unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
def SpotifyPlaylist(args: PlaylistAction) -> str:
    """Manage Spotify playlists with various actions."""
    logger.info(f"Playlist tool called with action: {args.action}")
    
    try:
        match args.action:
            case "get":
                logger.info("Getting current user's playlists")
                playlists = spotify_client.get_current_user_playlists()
                return json.dumps(playlists, indent=2)
                
            case "get_tracks":
                if not args.playlist_id:
                    logger.error("playlist_id is required for get_tracks action.")
                    return "playlist_id is required for get_tracks action."
                logger.info(f"Getting tracks in playlist: {args.playlist_id}")
                tracks = spotify_client.get_playlist_tracks(args.playlist_id)
                return json.dumps(tracks, indent=2)
                
            case "add_tracks":
                if not args.playlist_id or not args.track_ids:
                    return "playlist_id and track_ids are required for add_tracks action."
                logger.info(f"Adding tracks to playlist: {args.playlist_id}")
                spotify_client.add_tracks_to_playlist(
                    playlist_id=args.playlist_id,
                    track_ids=args.track_ids
                )
                return "Tracks added to playlist."
                
            case "remove_tracks":
                if not args.playlist_id or not args.track_ids:
                    return "playlist_id and track_ids are required for remove_tracks action."
                logger.info(f"Removing tracks from playlist: {args.playlist_id}")
                spotify_client.remove_tracks_from_playlist(
                    playlist_id=args.playlist_id,
                    track_ids=args.track_ids
                )
                return "Tracks removed from playlist."
                
            case "change_details":
                if not args.playlist_id:
                    logger.error("playlist_id is required for change_details action.")
                    return "playlist_id is required for change_details action."
                if not args.name and not args.description:
                    logger.error("At least one of name or description is required.")
                    return "At least one of name or description is required."
                
                logger.info(f"Changing playlist details: {args.playlist_id}")
                spotify_client.change_playlist_details(
                    playlist_id=args.playlist_id,
                    name=args.name,
                    description=args.description
                )
                return "Playlist details changed."
                
            case _:
                return f"Unknown playlist action: {args.action}. Supported actions are: get, get_tracks, add_tracks, remove_tracks, change_details."
                
    except SpotifyException as se:
        error_msg = f"Spotify Client error occurred: {str(se)}"
        logger.error(error_msg)
        return f"An error occurred with the Spotify Client: {str(se)}"
    except Exception as e:
        error_msg = f"Unexpected error occurred: {str(e)}"
        logger.error(error_msg)
        return error_msg

def main():
    print("Starting MCP server...")
    mcp.run()    

# if __name__ == "__main__":
#     print("Starting MCP server...")
#     mcp.run()
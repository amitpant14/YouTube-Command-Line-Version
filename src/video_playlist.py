"""A video playlist class."""
from typing import Dict
from .video import Video
class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_title: str):
        """Playlist constructor"""
        self._title = playlist_title
        self._videos = {}

    @property
    def title(self) -> str:
        """Returns the title of playlist."""
        return self._title

    @property
    def videos(self) -> Dict[str, Video]:
        """Returns the dictionary of videos."""
        return self._videos

    def add_video(self, video):
        """Adds the passed video to the videos dictionary
        
        Args:
            video: the video to be added
        """
        self._videos[video.video_id] = video

    def remove_video(self, video):
        """Removes the passed video from the videos dictionary
        
        Args:
            video: the video to be removed
        """
        self._videos.pop(video.video_id)

    def reset_playlist(self):
        """Resets the videos dictionary, hence the playlist"""
        self._videos = {}

    def get_all_videos(self):
        """returns the dictionary of videos"""
        return self._videos

    
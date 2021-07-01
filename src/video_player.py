"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist
from .command_parser import CommandException
from .command_parser import CommandParser

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._currently_playing_video = None
        self._current_video_status = None
        self._all_playlists = {}
        self._parser = CommandParser(self)

    def formatted_video_info(self, video):
        video_title = video.title
        video_id = video.video_id
        video_tags = " ".join(video.tags)
        return f"{video_title} ({video_id}) [{video_tags}]"

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        all_videos = sorted(all_videos, key = lambda x : x.title)
        print("Here's a list of all available videos:")
        for video in all_videos:
            video_flag_status = ""
            if video.flag_reason != "":
                video_flag_status = f" - FLAGGED (reason: {video.flag_reason})"
            print(f"{self.formatted_video_info(video)}{video_flag_status}")

    def play_video(self, video_id: str):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video_to_play = self._video_library.get_video(video_id)
        if video_to_play is None:
            print("Cannot play video: Video does not exist")
            return
        if video_to_play.flag_reason != "":
            print(f"Cannot play video: Video is currently flagged (reason: {video_to_play.flag_reason})")
            return
        if self._currently_playing_video is not None:
            print(f"Stopping video: {self._currently_playing_video.title}")
        print(f"Playing video: {video_to_play.title}")
        self._currently_playing_video = video_to_play
        self._current_video_status = 1

    def stop_video(self):
        """Stops the current video."""
        if self._currently_playing_video is None:
            print("Cannot stop video: No video is currently playing")
            return 
        print(f"Stopping video: {self._currently_playing_video.title}")
        self._currently_playing_video = None
        self._current_video_status = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = self._video_library.get_all_videos()
        non_flagged_videos = [video for video in all_videos if video.flag_reason == ""]
        if len(non_flagged_videos) == 0:
            print("No videos available")
            return
        random_video_id = random.choice(non_flagged_videos).video_id
        self.play_video(random_video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self._currently_playing_video is None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self._current_video_status == 0:
                print(f"Video already paused: {self._currently_playing_video.title}")
            else:
                self._current_video_status = 0
                print(f"Pausing video: {self._currently_playing_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if self._currently_playing_video is None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self._current_video_status == 1:
                print("Cannot continue video: Video is not paused")
            else:
                self._current_video_status = 1
                print(f"Continuing video: {self._currently_playing_video.title}")

    def show_playing(self):
        """Displays video currently playing."""
        if self._currently_playing_video is None:
            print("No video is currently playing")
        else:
            current_video_info = self.formatted_video_info(self._currently_playing_video)
            if self._current_video_status == 0:
                current_video_info = current_video_info + " - PAUSED"
            print(f"Currently playing: {current_video_info}")

    def create_playlist(self, playlist_name: str):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lower_case_playlist_name = playlist_name.lower()
        if lower_case_playlist_name in self._all_playlists:
            print("Cannot create playlist: A playlist with the same name already exists.")
        else:
            new_playlist = Playlist(playlist_name)
            self._all_playlists[lower_case_playlist_name] = new_playlist
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name: str, video_id: str):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        lower_case_playlist_name = playlist_name.lower()
        if lower_case_playlist_name not in self._all_playlists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return
        video_to_add = self._video_library.get_video(video_id)
        if video_to_add is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            if video_to_add.flag_reason != "":
                print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video_to_add.flag_reason})")
                return
            playlist_videos = self._all_playlists[lower_case_playlist_name].videos
            if video_id in playlist_videos:
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                self._all_playlists[lower_case_playlist_name].add_video(video_to_add)
                print(f"Added video to {playlist_name}: {video_to_add.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if not self._all_playlists:
            print("No playlists exist yet")
            return
        print("Showing all playlists:")
        for playlist in sorted(self._all_playlists.values(), key = lambda x : x.title):
            print(f"  {playlist.title}")

    def show_playlist(self, playlist_name: str):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lower_case_playlist_name = playlist_name.lower()
        if lower_case_playlist_name not in self._all_playlists:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return
        print(f"Showing playlist: {playlist_name}")
        required_playlist = self._all_playlists[lower_case_playlist_name]
        if not required_playlist.videos:
            print("  No videos here yet")
            return
        for video_id, video in required_playlist.videos.items():
            video_flag_status = ""
            if video.flag_reason != "":
                video_flag_status = f" - FLAGGED (reason: {video.flag_reason})"
            print(f"{self.formatted_video_info(video)}{video_flag_status}")

    def remove_from_playlist(self, playlist_name: str, video_id: str):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        lower_case_playlist_name = playlist_name.lower()
        if lower_case_playlist_name not in self._all_playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        video_to_add = self._video_library.get_video(video_id)
        if video_to_add is None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            playlist_videos = self._all_playlists[lower_case_playlist_name].videos
            if video_id not in playlist_videos:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                self._all_playlists[lower_case_playlist_name].remove_video(video_to_add)
                print(f"Removed video from {playlist_name}: {video_to_add.title}")

    def clear_playlist(self, playlist_name: str):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lower_case_playlist_name = playlist_name.lower()
        if lower_case_playlist_name not in self._all_playlists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        self._all_playlists[lower_case_playlist_name].reset_playlist()
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name: str):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lower_case_playlist_name = playlist_name.lower()
        if lower_case_playlist_name not in self._all_playlists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        self._all_playlists.pop(lower_case_playlist_name)
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term: str):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        matching_videos = []
        for video in all_videos:
            if video.flag_reason == "" and search_term.lower() in video.title.lower():
                matching_videos.append(video)
        if len(matching_videos) == 0:
            print(f"No search results for {search_term}")
            return
        maching_videos = sorted(matching_videos, key = lambda x : x.title)
        print(f"Here are the results for {search_term}:")
        for number, video in enumerate(matching_videos):
            print(f"{number+1}) {self.formatted_video_info(video)}")
        print("Would you like to play any of the above? If yes, specify the number of the video.\n If your answer is not a valid number, we will assume it's a no.")
        command = input()
        try:
            self._parser.process_command(command, matching_videos)
        except:
            return

    def search_videos_tag(self, video_tag: str):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        matching_videos = []
        for video in all_videos:
            if video.flag_reason != "":
                continue
            for tag in video.tags:
                if video_tag.lower() == tag.lower():
                    matching_videos.append(video)
                    break
        if len(matching_videos) == 0:
            print(f"No search results for {video_tag}")
            return
        maching_videos = sorted(matching_videos, key = lambda x : x.title)
        print(f"Here are the results for {video_tag}:")
        for number, video in enumerate(matching_videos):
            print(f"{number+1}) {self.formatted_video_info(video)}")
        print("Would you like to play any of the above? If yes, specify the number of the video.\n If your answer is not a valid number, we will assume it's a no.")
        command = input()
        try:
            self._parser.process_command(command, matching_videos)
        except:
            return

    def flag_video(self, video_id: str, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_to_flag = self._video_library.get_video(video_id)
        if video_to_flag is None:
            print("Cannot flag video: Video does not exist")
        elif video_to_flag.flag_reason != "":
            print("Cannot flag video: Video is already flagged")
        else:
            if self._currently_playing_video is not None and video_id == self._currently_playing_video.video_id:
                self.stop_video()
            video_to_flag.flag_reason = flag_reason if flag_reason != "" else "Not supplied"
            print(f"Successfully flagged video: {video_to_flag.title} (reason: {video_to_flag.flag_reason})")

    def allow_video(self, video_id: str):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video_to_unflag = self._video_library.get_video(video_id)
        if video_to_unflag is None:
            print("Cannot remove flag from video: Video does not exist")
        elif video_to_unflag.flag_reason == "":
            print("Cannot remove flag from video: Video is not flagged")
        else:
            video_to_unflag.flag_reason = ""
            print(f"Successfully removed flag from video: {video_to_unflag.title}")

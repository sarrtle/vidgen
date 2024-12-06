"""All Utility tools for this project."""

from os import listdir
from yt_dlp import YoutubeDL


def download_youtube_video(url: str):
    """Download a youtube video.

    Args:
        url (str): The URL string of the youtube video.

    """
    all_clips = listdir("assets/clips/")
    last_clip_number = len(all_clips) + 1
    options = {"format": "312", "outtmpl": f"assets/clips/clip{last_clip_number}.mp4"}

    with YoutubeDL(options) as ytdl:
        ytdl.download([url])

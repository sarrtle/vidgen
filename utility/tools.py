"""All Utility tools for this project."""

from os import listdir
from typing import Any, Callable, Literal
from customtkinter import CTkFont
from yt_dlp import YoutubeDL


def download_youtube_video(url: str, progress_hook: Callable[[dict[str, Any]], None]):
    """Download a youtube video.

    Args:
        url (str): The URL string of the youtube video.
        progress_hook (Callable[(dict[str, str], None)]): A callback function that provides
            updates on download progress for the user interface.

    """
    all_clips = listdir("assets/clips/")
    last_clip_number = len(all_clips) + 1
    options = {
        "format": "312",
        "outtmpl": f"assets/clips/clip{last_clip_number}.mp4",
        "progress_hooks": [progress_hook],
    }

    with YoutubeDL(options) as ytdl:
        ytdl.download([url])


def tkinter_font(size: int = 14, weight: Literal["normal", "bold"] = "normal"):
    """Create font with custom tkinter.

    Notes:
        This is for the desktop user interface only.

    """
    return CTkFont("assets/font/futura-extra-bold.ttf", size=size, weight=weight)


def human_readable_size(bytes_number: int):
    """Convert bytes into readable string."""
    if bytes_number > 1e6:
        return f"{bytes_number / 1e6:.2f} MB"
    elif bytes_number > 1e3:
        return f"{bytes_number / 1e3:.2f} KB"
    else:
        return f"{bytes_number} B"

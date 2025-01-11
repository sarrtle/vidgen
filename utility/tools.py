"""All Utility tools for this project."""

import hashlib
from os import listdir
from typing import Any, Callable, Literal

from customtkinter import CTkFont
from pygame import mixer
from yt_dlp import YoutubeDL

# initialize mixer for method play_voiceover
mixer.init()

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

def create_audio_filename(script: str, voice_model_name: str):
    """Create an audio filename with hash sha256.
    
    Converts the whole script into sha256 hexdigits for their
    unique filenames and easy to retain information.
    """
    def create_hash_content(string: str):
        hash_object = hashlib.sha256(string.encode())
        content_hash = hash_object.hexdigest()
        return content_hash

    hash_script = create_hash_content(script)
    hash_voice_model = create_hash_content(voice_model_name)

    return f"cache/audio_{hash_script}-{hash_voice_model}.mp3"

def play_voiceover(filepath: str) -> None:
    """Play the voiceover file with pygame.
    
    Notes:
        I have tried multiple libraries, only this
        one works.

    """
    mixer.music.load(filepath)
    mixer.music.play()

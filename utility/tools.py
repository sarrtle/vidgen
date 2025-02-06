"""All Utility tools for this project."""

import hashlib
from os import listdir
from typing import Any, Callable, Literal
from datetime import datetime

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

    Args:
        size (int): The size of the font.
        weight (Literal["normal", "bold"]): The weight of the font.

    Returns:
        CTkFont: The CTkFont object.

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


def create_hash_content(string: str):
    """Generate hash content from string.

    Args:
        string (str): The string to hash.

    Returns:
        str: The generated hash string.

    """
    hash_object = hashlib.sha256(string.encode())
    content_hash = hash_object.hexdigest()
    return content_hash


def create_audio_filename(script: str, voice_model_name: str) -> str:
    """Create an audio filename with hash sha256.

    Converts the whole script into sha256 hexdigits for their
    unique filenames and easy to retain information.

    Args:
        script (str): The generated or pasted script context.
        voice_model_name: The deepgram voice model name.

    Returns:
        str: The generated filepath

    """
    hash_script = create_hash_content(script)
    hash_voice_model = create_hash_content(voice_model_name)

    return f"cache/audio_{hash_script}-{hash_voice_model}.mp3"


def create_video_filename(filepath: str) -> str:
    """Create a video filename with hash sha256.

    Arts:
        filepath (str): The video file path.

    Returns:
        str: The generated filepath.

    """
    hash_video_file_path = create_hash_content(filepath)
    now = datetime.now()

    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

    return f"videos/video_{hash_video_file_path}-{timestamp}.mp4"


def play_voiceover(filepath: str) -> None:
    """Play the voiceover file with pygame.

    Args:
        filepath (str): The path of the audio.

    Notes:
        I have tried multiple libraries, only this
        one works.

    """
    mixer.music.load(filepath)
    mixer.music.play()

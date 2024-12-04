"""All Utility tools for this project."""

from os import listdir
from os.path import isfile
from yt_dlp import YoutubeDL

from json import dump, load

from models.config_model import ConfigData


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


def save_api_config(config_object: ConfigData):
    """Save your config file locally.

    Args:
        config_object (model.ConfigData): Config object.

    """
    data = {
        "api": {
            "deepinfra_token": config_object.deepinfra_token,
            "openai_token": config_object.openai_token,
            "deepgram_token": config_object.deepgram_token,
        },
        "default_settings": {
            "text_model": config_object.text_model,
            "voice_model": config_object.voice_model,
            "font": config_object.font,
            "text_position": config_object.text_position,
        },
    }

    with open("config.json", "w") as file:
        dump(data, file)


def load_config_object() -> ConfigData:
    """Load the config object."""
    if not isfile("config.json"):
        return ConfigData()

    with open("config.json", "r", encoding="utf-8") as file:
        config_data = load(file)

    return ConfigData(
        deepinfra_token=config_data["api"]["deepinfra_token"],
        openai_token=config_data["api"]["openai_token"],
        deepgram_token=config_data["api"]["deepgram_token"],
        text_model=config_data["default_settings"]["text_model"],
        voice_model=config_data["default_settings"]["voice_model"],
        font=config_data["default_settings"]["font"],
        text_position=config_data["default_settings"]["text_position"],
    )

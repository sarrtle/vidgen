"""All functions related to saving and loading configuration data."""

from os.path import isfile
from json import dump, load
from models.config_data import ApiDefaultSettings, ConfigData, StoryDefaultSettings


def save_api_config(config_object: ConfigData):
    """Save your config file locally.

    Args:
        config_object (model.ConfigData): Config object.

    """
    data = {
        "api_settings": {
            "gemini_text_model": config_object.api_settings.gemini_text_model,
            "gemini_vision_model": config_object.api_settings.gemini_vision_model,
            "gemini_token": config_object.api_settings.gemini_token,
            "deepinfra_text_model": config_object.api_settings.deepinfra_text_model,
            "deepinfra_vision_model": config_object.api_settings.deepinfra_vision_model,
            "deepinfra_token": config_object.api_settings.deepinfra_token,
            "openai_text_model": config_object.api_settings.openai_text_model,
            "openai_vision_model": config_object.api_settings.openai_vision_model,
            "openai_token": config_object.api_settings.openai_token,
            "deepgram_token": config_object.api_settings.deepgram_token,
        },
        "default_settings": {
            "story": {
                "theme": config_object.story_settings.theme,
                "text_model": config_object.story_settings.text_model,
                "voice_model": config_object.story_settings.voice_model,
                "font": config_object.story_settings.font,
                "text_position": config_object.story_settings.text_position,
                "text_color": config_object.story_settings.text_color,
                "text_style": config_object.story_settings.text_style,
                "text_stroke": config_object.story_settings.text_stroke,
            }
        },
    }

    with open("config.json", "w") as file:
        dump(data, file, indent=4)


def load_config_object() -> ConfigData:
    """Load the config object."""
    # return config data with default values
    if not isfile("config.json"):
        config_data = ConfigData(StoryDefaultSettings(), ApiDefaultSettings())
        save_api_config(config_data)
        return config_data

    # load config data locally from file
    with open("config.json", "r", encoding="utf-8") as file:
        config_data = load(file)

    # load the story settings
    story_settings = StoryDefaultSettings(
        theme=config_data["default_settings"]["story"]["theme"],
        text_model=config_data["default_settings"]["story"]["text_model"],
        voice_model=config_data["default_settings"]["story"]["voice_model"],
        font=config_data["default_settings"]["story"]["font"],
        text_position=config_data["default_settings"]["story"]["text_position"],
        text_color=config_data["default_settings"]["story"]["text_color"],
        text_style=config_data["default_settings"]["story"]["text_style"],
        text_stroke=config_data["default_settings"]["story"]["text_stroke"],
    )

    # load the api settings
    api_settings = ApiDefaultSettings(
        gemini_text_model=config_data["api_settings"]["gemini_text_model"],
        gemini_vision_model=config_data["api_settings"]["gemini_vision_model"],
        gemini_token=config_data["api_settings"]["gemini_token"],
        deepinfra_text_model=config_data["api_settings"]["deepinfra_text_model"],
        deepinfra_vision_model=config_data["api_settings"]["deepinfra_vision_model"],
        deepinfra_token=config_data["api_settings"]["deepinfra_token"],
        openai_text_model=config_data["api_settings"]["openai_text_model"],
        openai_vision_model=config_data["api_settings"]["openai_vision_model"],
        openai_token=config_data["api_settings"]["openai_token"],
        deepgram_token=config_data["api_settings"]["deepgram_token"],
    )

    return ConfigData(
        story_settings=story_settings,
        api_settings=api_settings,
    )

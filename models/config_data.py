"""Objects to be use in the project for easy access.

Classes:
    - ConfigData: The main configuration object for the entire project.
    - StoryDefaultSettings: Default settings data for the story window.

Todo:
    - Make all "required" values into another constant value or enumeration.

"""

from dataclasses import dataclass

from typing import Literal


@dataclass
class ConfigData:
    """The main configuration object for the entire project.

    Some values are the default values.
    """

    # forwarding reference the other class objects
    # default settings for other settings
    story_settings: "StoryDefaultSettings"
    api_settings: "ApiDefaultSettings"


@dataclass
class StoryDefaultSettings:
    """Default settings data for the story window."""

    # user settings for story window
    theme: Literal["Horror", "Facts"] = "Horror"
    text_model: Literal["DeepInfra", "Openai"] = "DeepInfra"
    voice_model: Literal["aura-arcas-en", "aura-luna-en", "aura-asteria-en"] = "aura-asteria-en"
    font: Literal["default", "Futura", "Monosans"] = "default"
    text_position: Literal["top", "center", "bottom"] = "center"
    text_color: Literal["white", "yellow", "violet", "blue"] = "yellow"
    text_style: Literal["1 word", "3 words"] = "3 words"
    text_stroke: int = 5


@dataclass
class ApiDefaultSettings:
    """Default settings data for the story window."""

    # gemini free model API settings
    gemini_text_model: Literal["Gemini-free"] = "Gemini-free"
    gemini_vision_model: Literal["Gemini-vision-free"] = "Gemini-vision-free"
    gemini_token: str | None = None

    # deepinfra api settings
    deepinfra_text_model: Literal["Llama-70b", "Llama-405b"] = "Llama-70b"
    deepinfra_vision_model: Literal["Llama-vision-vision-big", "Llama-vision-small"] = (
        "Llama-vision-vision-big"
    )
    deepinfra_token: str | None = None

    # openai api settings
    openai_text_model: Literal["Gpt-4o", "Gpt-4o-mini"] = "Gpt-4o"
    openai_vision_model: Literal["Gpt-4o", "Gpt-4o-mini"] = "Gpt-4o"
    openai_token: str | None = None

    # deepgram api settings
    deepgram_token: str | None = None

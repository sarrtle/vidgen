"""Objects to be use in the project for easy access.

Classes:
    - ConfigData: The main configuration object for the entire project.
    - StoryDefaultSettings: Default settings data for the story window.
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
    voice_model: Literal["Arceus", "Luna", "Asteria"] = "Arceus"
    font: Literal["default", "Futura", "Monosans"] = "default"
    text_position: Literal["top", "center", "bottom"] = "center"


@dataclass
class ApiDefaultSettings:
    """Default settings data for the story window."""

    # deepinfra api settings
    deepinfra_text_model: Literal["Llama", "Mixtral"] = "Llama"
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

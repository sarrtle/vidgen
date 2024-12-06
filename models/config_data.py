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

    # api values
    deepinfra_token: str | None = None
    openai_token: str | None = None
    deepgram_token: str | None = None


@dataclass
class StoryDefaultSettings:
    """Default settings data for the story window."""

    # user settings for story window
    theme: Literal["Horror", "Facts"] = "Horror"
    text_model: Literal["DeepInfra", "Openai"] = "DeepInfra"
    voice_model: Literal["Arceus", "Luna", "Asteria"] = "Arceus"
    font: Literal["default", "Futura", "Monosans"] = "default"
    text_position: Literal["top", "center", "bottom"] = "center"

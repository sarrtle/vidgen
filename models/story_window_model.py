"""All object models for Story Window component."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class StoryWindowValues:
    """Story window settings configurations."""

    theme: Literal["Horror", "Facts"]
    text_model: Literal["DeepInfra", "Openai"]
    idea: str
    context: str
    voice_model: Literal["Arceus", "Luna", "Asteria"]
    text_position: Literal["top", "center", "bottom"]
    text_font: Literal["default", "Futura", "Monosans"]

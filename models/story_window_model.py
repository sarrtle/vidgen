"""All object models for Story Window component."""

from dataclasses import dataclass
from typing import Literal



@dataclass
class StoryWindowValues:
    """Story window settings configurations."""

    theme: Literal["Horror", "Facts"]
    text_model: Literal["Gemini","DeepInfra", "Openai"]
    idea: str
    context: str
    voice_model: Literal["aura-arcas-en", "aura-luna-en", "aura-asteria-en"]
    text_position: Literal["top", "center", "bottom"]
    text_font: Literal["default", "Futura", "Monosans"]
    text_color: Literal["white", "yellow", "violet", "blue"]
    text_style: Literal["1 word", "3 words"]
    text_stroke: int

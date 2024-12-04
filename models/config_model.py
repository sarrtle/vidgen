"""Objects to be use in the project for easy access."""

from dataclasses import dataclass


@dataclass()
class ConfigData:
    """Config data and some settings.

    Some values are the default values.
    """

    deepinfra_token: str | None = None
    openai_token: str | None = None
    deepgram_token: str | None = None
    text_model: str = "deepinfra"
    voice_model: str = "arceus"
    font: str = "default"
    text_position: str = "center"

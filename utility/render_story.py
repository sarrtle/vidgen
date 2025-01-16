"""Module for rendering the story video."""

from models.config_data import ConfigData
from utility.generate_voice import GenerateVoice
from utility.vidgen_api import VidGen


class RenderStory:
    """RenderStory object.

    Attributes:
        - chacha

    """

    def __init__(self, script: str, config_data: ConfigData, video_file_clip: VidGen):
        """Initialize RenderStory.

        Args:
            script (str): The generated or pasted script context story.
            config_data (models.ConfigData): The project configurations.
            video_file_clip (utility.Vidgen): The initialized Vidgen object.

        """
        self._script: str = script
        self._config_data: ConfigData = config_data
        self._video_file_clip: VidGen = video_file_clip

    def render(self):
        """Render the video."""
        # get audio transcription data
        generate_voice_object = GenerateVoice(
            script=self._script, config_data=self._config_data
        )
        audio_transcription_data = generate_voice_object.transcript()

        words = audio_transcription_data["results"]["channels"][0]["alternatives"][0][
            "words"
        ]

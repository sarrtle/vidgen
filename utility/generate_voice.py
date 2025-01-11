"""Voice generation module."""

from tkinter import messagebox
from deepgram import DeepgramApiError, DeepgramApiKeyError, DeepgramClient, DeepgramUnknownApiError, SpeakOptions

from models.config_data import ConfigData


from utility.tools import create_audio_filename


class GenerateVoice:
    """Generate a voiceover from script."""

    def __init__(self, script: str, config_data: ConfigData):
        """Initialize GenerateVoice.

        Args:
            script (str): The AI generated script from idea context.
            config_data (models.ConfigData): The config object used from the system.

        """
        self._script: str = script
        self._config_data: ConfigData = config_data

    def generate(self) -> bool:
        """Generate the voiceover.

        Returns:
            bool: The status if API request succeeded.

        Notes:
            Currently, I will be using the one time request instead of
            chunking the voiceover by sentence to make the process more
            faster. Chunking and merging voiceover by sentence will make
            the voice realisting and easy to understand.

        """
        # preparing options and filename
        speak_options = {"text": self._script}
        filename = create_audio_filename(script=self._script, voice_model_name=self._config_data.story_settings.voice_model)

        # Initialize deepgram
        deepgram = DeepgramClient(api_key=self._config_data.api_settings.deepgram_token)

        # choose model
        options = SpeakOptions(model=self._config_data.story_settings.voice_model)
        
        # WARNING AND TODO: catch more error for deepgram error

        # request to the deepgram api sdk
        try:
            deepgram.speak.rest.v("1").save(filename, speak_options, options)
        except (DeepgramApiError, DeepgramApiKeyError, DeepgramUnknownApiError) as exc:
            if isinstance(exc, DeepgramApiKeyError):
                messagebox.showerror(title="Error", message=str(exc))
            else:
                messagebox.showerror(title="Error", message=exc.message)
            return False

        return True

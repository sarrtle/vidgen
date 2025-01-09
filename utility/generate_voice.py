"""Voice generation module."""

from tkinter import messagebox
from deepgram import DeepgramClient, SpeakOptions

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

    def generate(self):
        """Generate the voiceover.

        Notes:
            Currently, I will be using the one time request instead of
            chunking the voiceover by sentence to make the process more
            faster. Chunking and merging voiceover by sentence will make
            the voice realisting and easy to understand.

        """
        # check if token is valid
        if not self._config_data.api_settings.deepgram_token:
            messagebox.showerror(title="No deepgram token!", message="Please input deepgram API token first.")
            return
        
        # preparing options and filename
        speak_options = {"text": self._script}
        filename = create_audio_filename(script=self._script, voice_model_name=self._config_data.story_settings.voice_model)

        # Initialize deepgram
        deepgram = DeepgramClient(api_key=self._config_data.api_settings.deepgram_token)

        # choose model
        options = SpeakOptions(model=self._config_data.story_settings.voice_model)
        
        # WARNING AND TODO: There is seem to be no error information on their
        #   documentation, so watch out from whatever errors here.

        # request to the deepgram api sdk
        deepgram.speak.rest.v("1").save(filename, speak_options, options)

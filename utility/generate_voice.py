"""Voice generation module."""

from tkinter import messagebox
from deepgram import DeepgramClient, SpeakOptions

from models.config_data import ConfigData

import hashlib


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

    def _generate(self):
        """Generate the voiceover.

        Notes:
            Currently, I will be using the one time request instead of
            chunking the voiceover by sentence to make the process more
            faster. Chunking and merging voiceover by sentence will make
            the voice realisting and easy to understand.

        """
        # check if token is valid
        if self._config_data.api_settings.deepgram_token is None:
            messagebox.showerror(title="No deepgram token!", message="Please input deepgram API token first.")
            return
        
        # preparing options and filename
        speak_options = {"text": self._script}

        # generate a unique filename for the audio base on script
        hash_object = hashlib.sha256(self._script.encode())
        content_hash = hash_object.hexdigest()
        filename = f"cache/audio_{content_hash}.mp3"

        # Initialize deepgram
        deepgram = DeepgramClient(api_key=self._config_data.api_settings.deepgram_token)

        # choose model
        options = SpeakOptions(model=self._config_data.story_settings.voice_model)
        
        # WARNING AND TODO: There is seem to be no error information on their
        #   documentation, so watch out from whatever errors here.

        # request to the deepgram api sdk
        response = deepgram.speak.rest.v("1").save(filename, speak_options, options)
        print(response.to_json(indent=4))

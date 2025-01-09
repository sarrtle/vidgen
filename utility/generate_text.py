"""Generate text module."""

from typing import Callable, Literal
import google.generativeai as genai

from models.config_data import ConfigData
from models.prompt import GeneratePrompt

class GenerateText:
    """The base class of all text generation models.
    
    Will use different models according to the configuration files.
    """

    def __init__(self, idea: str, config_object: ConfigData, done_callback: Callable[[str, bool, str | None, str | None], None]):
        """Initialize GenerateText."""
        self._idea: str = idea
        self._config_object: ConfigData = config_object
        self._theme: Literal["Horror", "Facts"] = self._config_object.story_settings.theme
        self._done_callback: Callable[[str, bool, str | None, str | None], None] = done_callback

        # generate prompt
        self._prompt: str = GeneratePrompt(idea=self._idea, theme=self._config_object.story_settings.theme).get()

    def _on_gemini_service(self):
        """Request on API using Gemini service.
        
        Will return boolean for the statuses response, if something
        went wrong, it will handled by the tkinter.messagebox for
        showing the error or warning.

        Returns:
            str: The generated response, if error or something went wrong,
                then will return an empty string.

        """
        # handle error for no token on gemini
        if not self._config_object.api_settings.gemini_token:
            self._done_callback("", True, "No gemini token found!", "Please input your gemini token first.")
            return

        # intiate and configuregemini
        genai.configure(api_key=self._config_object.api_settings.gemini_token)
        model = genai.GenerativeModel(model_name=self._config_object.api_settings.gemini_text_model, system_instruction=self._prompt)

        response = model.generate_content(contents="What happened?")

        self._done_callback(response.text, False, None, None)

    def _on_no_service(self):
        """Return proper callback if a model is not yet implemented."""
        self._done_callback("", True, "No model available!", "This model is not yet implemented")

    def request(self):
        """Request to their respective API.

        Warning:
            This function must run on thread. Because
            it is a blocking thread and not asynchronous.
        
        Returns:
            str: The generated text.

        """
        chosen_service = self._config_object.story_settings.text_model
        
        if chosen_service == "Gemini":
            self._on_gemini_service()
        
        # if some models are not yet implemented
        else:
            self._on_no_service()


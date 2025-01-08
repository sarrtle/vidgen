"""Prompt model for text generation."""


from typing import Literal


class GeneratePrompt:
    """Generate a prompt base on given idea."""

    def __init__(self, idea: str, theme: Literal["Horror", "Facts"] = "Horror"):
        """Initialize GeneratePrompt.
        
        Args:
            idea (str): The given idea to be use in prompt.
            theme (Literal["Horror", "Facts"]): The chosen theme from config data

        """
        self._prompt: str = ""
        if theme == "Horror":
            self._prompt = f"""Using this story idea: "{idea}". The first sentence of the
            story is about the summarization of the whole story that hooks listener and doesn't 
            spoil the rest of the story, don't include time and place. Then incorporate the body
            with climax and the ending. Make the story intense and heart throbbing scenes. It must
            be in paragraph format. This story will be put in youtube shorts, facebook page, instagram
            reels and tiktok so don't create too long above 60 seconds of speaking with your story."""
        elif theme == "Facts":
            self._prompt = "TODO: Do the facts prompt here."

    def get(self):
        """Get the prompt as string format.
        
        Returns:
            str: The formatted prompt.

        """
        return self._prompt


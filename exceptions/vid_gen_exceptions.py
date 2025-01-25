"""All class Exceptions to be use in this project."""


class NoVideoFileClip(Exception):
    """Raise and error if no video was loaded yet on VidGen."""

    def __init__(self, message: str = "No Video was loaded before.") -> None:
        self.message = message
        super().__init__(self.message)


class NoAudioFileClip(Exception):
    """Raise and error if no audio was loaded yet on VidGen."""

    def __init__(self, message: str = "No Audio was loaded before.") -> None:
        self.message = message
        super().__init__(self.message)

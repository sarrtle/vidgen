"""All class Exceptions to be use in this project."""


class NoVideoFileCLip(Exception):
    """Raise and error if no video was loaded yet on VidGen."""

    def __init__(self, message: str = "No Video was loaded before.") -> None:
        self.message = message
        super().__init__(self.message)

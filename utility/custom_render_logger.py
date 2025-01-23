"""Custom moviepy rendering indicator."""

from typing import Any, override
from customtkinter import CTkLabel, Variable
from proglog import ProgressBarLogger


class CustomMoviepyLogger(ProgressBarLogger):
    """Custom logger for moviepy rendering."""

    def __init__(
        self, progress_bar_variable: Variable, progress_label_variable: CTkLabel
    ):
        """Initialize custom logger for moviepy."""
        super().__init__()

        self._progress_bar_variable: Variable = progress_bar_variable
        self._progress_label_variable: CTkLabel = progress_label_variable

    @override
    def bars_callback(self, bar: str, attr: str, value: int, old_value: Any = None):
        """Create a custom indicator."""
        total_frames = self.bars[bar]["total"]
        percentage = value / total_frames
        percentage = round(percentage, 2)

        current_frame = value

        # apply percentage and frame values on user interface
        self._progress_bar_variable.set(value=percentage)
        self._progress_label_variable.configure(text=f"{current_frame}/{total_frames}")

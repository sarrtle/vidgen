"""A not yet available window for sidebar menu."""

from typing import Any
from customtkinter import CTkFrame, CTkLabel

from utility.tools import tkinter_font


class NoWindow(CTkFrame):
    """NoWindow class."""

    def __init__(self, master: CTkFrame, **kwargs: Any):
        """Initialize NoWindow.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            **kwargs (Any): What CtkFrame needs.

        Note:
            Any changes made when packing or rendering the
            component or widget are done on the method:
            `NoWindow.render`

        """
        super().__init__(master, **kwargs)
        self.name: str = "NoWindow"

        # set up widgets
        self._setup_content()

    def _setup_content(self):
        """Set up the widget content."""
        CTkLabel(
            master=self,
            text="This feature is not available yet.",
            font=tkinter_font(16, "bold"),
        ).pack(expand=True, fill="both", anchor="center")

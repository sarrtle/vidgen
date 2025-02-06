"""Sidebar components for desktop UI using tkinter.

Classes:
    Sidebar: The default sidebar component to use externally.
    _SidebarButton: Internal class for rendering sidebar buttons.

Notes:
    - `Sidebar` is for external use, providing a complete sidebar UI.
    - `_SidebarButton` is only for internal use within `Sidebar`.

"""

from typing import Any, Callable, override
from collections.abc import Sequence
from customtkinter import CTkButton, CTkFrame, ThemeManager


class _SidebarButton(CTkButton):
    """Sidebar button for the sidebar component.

    This is only for the Sidebar class to use.

    Attributes:
        text (str): The text on the button.

    Methods:
        pack(**kwargs: Any): Render the component to the sidebar frame.

    """

    def __init__(
        self, master: CTkFrame, text: str, command: Callable[[], None], **kwargs: Any
    ):
        """Initialize the _SidebarButton.

        Args:
            master (customtkinter.CtkFrame): The Sidebar frame.
            text (str): The text on the button.
            command (Callable[[], None]): The command to execute.
            **kwargs (Any): What CtkFrame needs.

        Notes:
            All sidebar buttons are inside the Sidebar._inner_frame variable
            for some design purposes.

        """
        super().__init__(
            master, text=text, fg_color="transparent", command=command, **kwargs
        )

        self.text: str = text

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the sidebar frame."""
        super().pack(pady=4)


class Sidebar(CTkFrame):
    """Sidebar component.

    Methods:
        on_select_sidebar_button(button_text: str): Do something when one of the sidebar button was selected.
        register_components(list_objects: Sequence[CTkFrame]): Register all sidebar componets.
        pack(**kwargs: Any): Render the component to the main window.

    """

    def __init__(self, master: CTkFrame, **kwargs: Any):
        """Initialize Sidebar.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            **kwargs (Any): What CtkFrame needs.

        Note:
            All sidebar buttons are inside the Sidebar._inner_frame variable
            for some design purposes.

        """
        super().__init__(master, **kwargs)
        self._master_frame: CTkFrame = master
        self._inner_frame: CTkFrame = CTkFrame(master=self, fg_color="transparent")
        self._inner_frame.pack(fill="both", expand=True, padx=15, pady=20)

        # important variables
        self._sidebar_components: Sequence[CTkFrame] = []
        self._previous_selected: CTkFrame

        # add sidebar buttons
        self._sidebar_buttons: list[_SidebarButton] = []
        self._add_sidebar_buttons()

    def _add_sidebar_buttons(self):
        """Add the sidebar buttons dynamically."""
        sidebar_names = ["Create", "Videos", "Clips", "Api"]

        for sidebar_name in sidebar_names:
            sidebar_button = _SidebarButton(
                master=self._inner_frame,
                text=sidebar_name,
                command=lambda name=sidebar_name: self.on_select_sidebar_button(name),
            )

            # render buttons to sidebar frame
            sidebar_button.pack()

            # register the buttons for future references
            self._sidebar_buttons.append(sidebar_button)

    def on_select_sidebar_button(self, button_text: str):
        """Do something when one of the sidebar button was selected.

        Args:
            button_text (str): The text on the button.

        """
        for button in self._sidebar_buttons:
            if button.text == button_text:
                # TODO: Get theme or original color as utility
                button.configure(
                    fg_color=ThemeManager.theme["CTkButton"]["fg_color"],
                    hover=False,
                )

                # don't do anything if same button was selected
                if self._previous_selected.__dict__.get("name") == button_text:
                    continue

                # get selected sidebar component
                current_selected = None

                for sidebar_component in self._sidebar_components:
                    if sidebar_component.__dict__.get("name") == button_text:
                        current_selected = sidebar_component

                if current_selected is None:
                    current_selected = self._previous_selected

                # remove the previous selected
                self._previous_selected.pack_forget()
                self._previous_selected = current_selected

                # add the new selected
                current_selected.pack(expand=True, fill="both")
            else:
                button.configure(fg_color="transparent", hover=True)

    def register_components(self, list_objects: Sequence[CTkFrame]):
        """Register all sidebar componets.

        All components will be use later for showing and hiding
        windows while clicking sidebar buttons.

        Args:
            list_objects (Sequence[CTkFrame]): The list of components.

        """
        self._sidebar_components = list_objects
        self._previous_selected = list_objects[0]

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the main window."""
        super().pack(fill="y", side="left", anchor="w")

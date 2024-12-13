"""Sidebar components for desktop UI using tkinter.

Classes:
    Sidebar: The default sidebar component to use externally.
    _SidebarButton: Internal class for rendering sidebar buttons.

Notes:
    - `Sidebar` is for external use, providing a complete sidebar UI.
    - `_SidebarButton` is only for internal use within `Sidebar`.

"""

from typing import Any, override
from collections.abc import Sequence
from customtkinter import CTkButton, CTkFrame, ThemeManager


class _SidebarButton(CTkButton):
    """Sidebar button for the sidebar component.

    This is only for the Sidebar class to use.
    """

    def __init__(self, master: CTkFrame, text: str, **kwargs: Any):
        """Initialize the _SidebarButton.

        Args:
            master (customtkinter.CtkFrame): The Sidebar frame.
            text (str): The text on the button.
            selected (bool): If the button is selected.
            **kwargs (Any): What CtkFrame needs.

        Notes:
            Any changes made when packing or rendering the
            component or widget are done on the method:
            `Sidebar.render`

            All sidebar buttons are inside the Sidebar._inner_frame variable
            for some design purposes.

        """
        super().__init__(master, text=text, fg_color="transparent", **kwargs)

        self.text: str = text

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the sidebar frame."""
        super().pack(pady=4)


class Sidebar(CTkFrame):
    """Sidebar component."""

    def __init__(self, master: CTkFrame, **kwargs: Any):
        """Initialize Sidebar.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            **kwargs (Any): What CtkFrame needs.

        Note:
            Any changes made when packing or rendering the
            component or widget are done on the method:
            `Sidebar.render`

            All sidebar buttons are inside the Sidebar._inner_frame variable
            for some design purposes.

        """
        super().__init__(master, **kwargs)

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
        story_button = _SidebarButton(master=self._inner_frame, text="Story")
        riddle_button = _SidebarButton(master=self._inner_frame, text="Riddle")
        music_button = _SidebarButton(master=self._inner_frame, text="Music")
        video_button = _SidebarButton(master=self._inner_frame, text="Videos")
        clip_button = _SidebarButton(master=self._inner_frame, text="Clips")
        api_button = _SidebarButton(master=self._inner_frame, text="Api")

        # register the on click command
        # I don't know why the loop method of registration won't work. Even I made copies
        # of object. The last iteration of the loop (upload) is always used as the selected
        # sidebar button.
        story_button.configure(command=lambda: self.on_select_sidebar_button("Story"))
        riddle_button.configure(command=lambda: self.on_select_sidebar_button("Riddle"))
        music_button.configure(command=lambda: self.on_select_sidebar_button("Music"))
        video_button.configure(command=lambda: self.on_select_sidebar_button("Videos"))
        clip_button.configure(command=lambda: self.on_select_sidebar_button("Clips"))
        api_button.configure(command=lambda: self.on_select_sidebar_button("Api"))

        # register the buttons for future references.
        self._sidebar_buttons = [
            story_button,
            riddle_button,
            music_button,
            video_button,
            clip_button,
            api_button,
        ]

        # render buttons to the sidebar frame
        story_button.pack()
        riddle_button.pack()
        music_button.pack()
        video_button.pack()
        clip_button.pack()
        api_button.pack()

    def on_select_sidebar_button(self, button_text: str):
        """Do something when one of the sidebar button was selected."""
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

                # assert (
                #     current_selected is not None
                # ), f"No attribute `name` on {button.text}."
                # TODO: Once all sidebar components has been made,
                #       uncomment assertion for checking of attribute `name`
                #       remove this temporary line of code
                if current_selected is None:
                    current_selected = self._previous_selected

                # remove the previous selected
                self._previous_selected.pack_forget()
                self._previous_selected = current_selected

                # add the new selected
                current_selected.pack()
            else:
                button.configure(fg_color="transparent", hover=True)

    def register_components(self, list_objects: Sequence[CTkFrame]):
        """Register all sidebar componets.

        All components will be use later for showing and hiding
        windows while clicking sidebar buttons.
        """
        self._sidebar_components = list_objects
        self._previous_selected = list_objects[0]

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the main window."""
        super().pack(fill="y", side="left", anchor="w")

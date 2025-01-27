"""Video section from the sidebar menu.

Shows all the generated videos from the assets/videos
and can delete or upload to social medias.
"""

from os import listdir, path
from typing import Any
from PIL import Image
from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkScrollableFrame,
    ThemeManager,
)

from models.config_data import ConfigData
from utility.tools import tkinter_font


class VideoWindow(CTkFrame):
    """Video window content."""

    def __init__(self, master: CTkFrame, config_data: ConfigData, **kwargs: Any):
        """Initialize VideoWindow.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            config_data (models.config_data.ConfigData): For saving and loading
                configurations.
            **kwargs (Any): What CTkFrame needs.

        """
        super().__init__(master, **kwargs)
        self.name: str = "Videos"

        # containers
        self._left_container: CTkFrame
        self._right_container: CTkFrame
        self._video_list_container: CTkScrollableFrame
        self._right_inner_container: CTkFrame
        self._right_button_list_container: CTkFrame

        # checker variables
        self._previous_selected: CTkButton | None = None

        # important variables
        self._preview_image_label: CTkLabel

        # setup containers
        self._setup_containers()

    def _setup_containers(self):
        """Set up important containers."""
        # left container
        self._left_container = CTkFrame(master=self, width=300)
        self._left_container.pack_propagate(False)
        self._left_container.pack(expand=False, fill="y", side="left", anchor="w")

        # right container
        self._right_container = CTkFrame(master=self)
        self._right_container.pack(expand=True, fill="both", side="left", anchor="w")

        # set up widgets of containers
        self._setup_left_container_widgets()
        self._setup_right_container_widgets()

    def _setup_left_container_widgets(self):
        """Set up left container widgets."""
        CTkLabel(
            master=self._left_container, text="Videos", font=tkinter_font(16, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 0))

        # video list
        self._video_list_container = CTkScrollableFrame(
            master=self._left_container, fg_color="transparent"
        )
        self._video_list_container.pack(fill="x", anchor="w", padx=12)

        # load videos to ui
        self._load_videos_to_ui()

    def _setup_right_container_widgets(self):
        """Set up right container widgets."""
        # centered inner container for right container
        inner_container = CTkFrame(master=self._right_container)
        inner_container.pack(fill="both", expand=True)

        image_object = Image.open("assets/preview/default.png")
        image = CTkImage(
            light_image=image_object, dark_image=image_object, size=(200, 420)
        )
        self._preview_image_label = CTkLabel(
            master=inner_container,
            text="Preview",
            image=image,
            width=250,
        )
        self._preview_image_label.pack(side="left", expand=False)

        option_frame = CTkFrame(master=inner_container, fg_color="transparent")
        option_frame.pack(side="left", expand=True, fill="both")

        center_option_frame = CTkFrame(master=option_frame)
        center_option_frame.pack(anchor="center", expand=True, fill="none")

        CTkLabel(master=center_option_frame, text="Options").pack(
            side="left", anchor="w", padx=12, pady=12
        )
        CTkLabel(master=center_option_frame, text="Delete").pack(
            anchor="w", padx=12, pady=12
        )

    def _load_videos_to_ui(self):
        """Load videos to ui."""
        video_list = listdir("videos/")

        for video in video_list:
            video_path = path.join("videos/", video)
            video_show_name = video[:5] + "..." + video[65:]
            video_widget = CTkButton(
                master=self._video_list_container,
                text=video_show_name,
                anchor="w",
                fg_color="transparent",
            )
            video_widget.pack(anchor="w", fill="x")
            video_widget.configure(
                command=lambda widget=video_widget: self._on_video_clicked(widget)
            )

    # button commands
    def _on_video_clicked(self, widget: CTkButton):
        """Handle when video was clicked.

        Args:
            widget (customtkinter.CTkButton): The widget button of a video.

        """
        # TODO: load an image

        # don't process on same widget clicked
        if self._previous_selected and self._previous_selected == widget:
            return

        if self._previous_selected:
            self._previous_selected.configure(fg_color="transparent", hover=True)

        widget.configure(
            fg_color=ThemeManager.theme["CTkButton"]["fg_color"], hover=False
        )

        self._previous_selected = widget

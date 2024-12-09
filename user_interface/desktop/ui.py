"""Desktop user interface.

Supports Windows / Mac / Linux.
"""

from collections.abc import Sequence
from PIL import Image
from customtkinter import CTk, CTkFrame, CTkLabel, CTkTextbox

from models.config_data import ConfigData
from user_interface.desktop.components.api_window import ApiWindow
from user_interface.desktop.components.sidebar import Sidebar
from user_interface.desktop.components.story_window import StoryWindow
from utility.config_tools import load_config_object
from utility.vidgen_api import VidGen

import platform

# incase needing to change the desktop size for big monitors.
DESKTOP_WIDTH = 1280
DESKTOP_HEIGHT = 720


class DesktopApp(CTk):
    """Main program for the desktop application."""

    def __init__(self):
        """Initialize the DesktopApp."""
        super().__init__()

        # basic configurations
        self.title("Vidgen")
        self.geometry(f"{DESKTOP_WIDTH}x{DESKTOP_HEIGHT}")

        if platform.system() == "Linux":
            self.attributes("-type", "utility")

        # load some important variables
        self._video_file_clip: VidGen = VidGen()
        self._default_preview_image: Image.Image = Image.open(
            "assets/preview/default.png"
        )
        self._config_object: ConfigData = load_config_object()
        self._default_font: str = "assets/fonts/futura-extra-bold.ttf"

        # Main frames
        self._right_side_container: CTkFrame | None = None

        # control widgets that needed to edit
        self._image_preview_widget: CTkLabel | None = None
        self._textbox_widget: CTkTextbox | None = None

        # initialize widgets and important functions
        self._setup_window()

    def _setup_window(self):
        """Set up frames of the window."""
        # main window
        main_window_frame = CTkFrame(master=self)
        main_window_frame.pack(fill="both", expand=True)

        # sidebar window
        sidebar = Sidebar(master=main_window_frame)
        sidebar.pack()

        # sidebar default content
        story_window = StoryWindow(
            master=main_window_frame, config_data=self._config_object
        )
        story_window.pack()

        api_window = ApiWindow(
            master=main_window_frame, config_data=self._config_object
        )

        components: Sequence[CTkFrame] = [story_window, api_window]
        sidebar.register_components(components)

        # default selection
        sidebar.on_select_sidebar_button("Story")

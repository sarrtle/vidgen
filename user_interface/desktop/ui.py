"""Desktop user interface.

Supports Windows / Mac / Linux.
"""

from PIL import Image
from customtkinter import CTk, CTkFrame, CTkLabel, CTkTextbox

from models.config_model import ConfigData
from user_interface.desktop.components.sidebar import Sidebar
from user_interface.desktop.components.story_window import StoryWindow
from utility.tools import load_config_object
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
        sidebar.render()

        # sidebar default content
        story_window = StoryWindow(master=main_window_frame)
        story_window.render()

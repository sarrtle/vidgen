"""Clips section from the sidebar menu.

Shows all the available clips from the assets/clips
or download new clips using yt-dlp.
"""

from os import listdir, remove
from os.path import isfile, join
from platform import system
import threading
from typing import Any, override
from customtkinter import (
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkProgressBar,
    CTkScrollableFrame,
    CTkToplevel,
    ThemeManager,
    Variable,
)
from tkinter import messagebox
from PIL import Image

from models.config_data import ConfigData
from utility.tools import download_youtube_video, human_readable_size, tkinter_font
from utility.vidgen_api import VidGen

EXAMPLE_YOUTUBE_LINKS = [
    # Note:
    # All links here are provided by the author and are safe.
    # Be cautious when accessing links if this section has been modified
    # by anyone other than the author or trusted contributors.
    # Special thanks to @GameplaysForFree for providing the gameplay: https://www.youtube.com/@GameplaysForFree-hr9bs
    "https://youtu.be/r5utBFtLtWk?si=IGOz2o5yT1drGnfr",
    "https://youtu.be/oPz7Uh_6ey4?si=ZfBCPE7okCSCuRhL",
    "https://youtu.be/GA8vYmmvqEk?si=OzGs0whFq6z_8JcD",
    "https://youtu.be/dBE0pZtK3ao?si=-8UqovyN7aGg-cps",
    "https://youtu.be/wv8_ePzdMv8?si=54LrqSiQuh4Ytwwq",
]


class ClipsWindow(CTkFrame):
    """Clips window content."""

    def __init__(self, master: CTkFrame, config_data: ConfigData, **kwargs: Any):
        """Initialize ClipsWindow.

        Args:
            master (customtkinter.CTkFrame): The main window of the desktop.
            config_data (models.config_data.ConfigData): For saving and loading configurations.
            **kwargs (Any): What CTkFrame needs.

        """
        super().__init__(master, **kwargs)
        self.name: str = "Clips"

        # containers
        self._left_container: CTkFrame
        self._left_container_inner_left: CTkFrame
        self._left_container_inner_right: CTkFrame
        self._clip_list_container: CTkScrollableFrame
        self._right_container: CTkFrame

        # some values needed
        self._link_entry: CTkEntry

        # important variables
        self._config_data: ConfigData = config_data
        self._clip_list_widgets: list[CTkButton] = []
        self._previous_selected: CTkButton | None = None
        self._clip_thumbnail_preview: CTkLabel
        self._progress_variable: Variable = Variable(value=0)

        # setup containers
        self._setup_containers()

    def _setup_containers(self):
        """Set up important containers."""
        # left container
        self._left_container = CTkFrame(master=self)
        self._left_container.pack(expand=True, fill="both", side="left")

        # left side of left container
        self._left_container_inner_left = CTkFrame(
            master=self._left_container, fg_color="transparent"
        )
        self._left_container_inner_left.pack(expand=True, fill="both", side="left")

        # right side of left container
        self._left_container_inner_right = CTkFrame(
            master=self._left_container, width=300, height=720
        )
        self._left_container_inner_right.pack_propagate(False)
        self._left_container_inner_right.pack(padx=(0, 14))

        # right container
        self._right_container = CTkFrame(master=self, width=300, height=340)
        self._right_container.pack_propagate(False)
        self._right_container.pack(padx=20, pady=20)

        # set up widgets of containers
        self._setup_left_container_inner_left_widgets()
        self._setup_left_container_inner_right_widgets()
        self._setup_right_container_widgets()

    def _setup_left_container_inner_left_widgets(self):
        """Set up widgets for the left side of container on inner left."""
        CTkLabel(
            master=self._left_container_inner_left,
            text="Clips",
            font=tkinter_font(weight="bold"),
        ).pack(anchor="w", padx=20, pady=(20, 0))

        self._clip_list_container = CTkScrollableFrame(
            master=self._left_container_inner_left
        )
        self._clip_list_container.pack(fill="both")

        # load clips to ui
        self._load_clips_to_ui()

    def _setup_left_container_inner_right_widgets(self):
        """Set up widgets for the lest side of container on inner left.

        Notes:
            gaps between widgets are 8 pixel.

        """
        center_frame = CTkFrame(
            master=self._left_container_inner_right, fg_color="transparent"
        )
        center_frame.pack(expand=True, anchor="center")

        # load image preview
        image_bytes = Image.open("assets/preview/default.png")
        default_image = CTkImage(
            light_image=image_bytes, dark_image=image_bytes, size=(200, 420)
        )
        self._clip_thumbnail_preview = CTkLabel(
            master=center_frame, text="Preview", image=default_image
        )
        self._clip_thumbnail_preview.pack(pady=(0, 8))

        CTkButton(master=center_frame, text="play").pack(fill="x", pady=(0, 8))
        CTkButton(
            master=center_frame,
            text="delete",
            fg_color="transparent",
            border_width=1,
            border_color="gray",
            command=self._on_delete_clip_clicked,
        ).pack(fill="x")

    def _load_clips_to_ui(self):
        """Load clips as list to UI.

        Notes:
            Loaded clips are not videos but as text.

            The thumbnails are only shown after clicking them
            so they are temporarily loaded one by one, and freeing
            them after not showing.

        """
        # remove the current clip widgets
        for clip_widget in self._clip_list_widgets:
            clip_widget.destroy()

        # refresh the clips
        list_of_clips = listdir("assets/clips/")

        for clip_name in list_of_clips:
            clip_widget = CTkButton(
                master=self._clip_list_container,
                text=clip_name,
                anchor="w",
                fg_color="transparent",
            )
            clip_widget.pack(padx=(8, 0), anchor="w", fill="x")
            clip_widget.configure(
                command=lambda widget=clip_widget: self._on_clip_clicked(widget)
            )

            self._clip_list_widgets.append(clip_widget)

    def _setup_right_container_widgets(self):
        """Set up widgets for the right side of container.

        Notes:
            Gaps are 8 pixels between widgets.

        """
        # add beautiful inner padding
        right_container_inner_frame = CTkFrame(
            master=self._right_container, fg_color="transparent"
        )
        right_container_inner_frame.pack(padx=20, pady=20, fill="both")

        # Download youtube from link
        CTkLabel(
            master=right_container_inner_frame,
            text="Download clip",
            font=tkinter_font(size=16, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))
        self._link_entry = CTkEntry(
            master=right_container_inner_frame, placeholder_text="enter youtube url"
        )
        self._link_entry.pack(fill="x", pady=(0, 8))
        CTkButton(
            master=right_container_inner_frame,
            text="download",
            command=self._on_download_clip_clicked,
        ).pack(anchor="e", pady=(0, 8), fill="x")

        # Add example urls that are useful
        CTkLabel(
            master=right_container_inner_frame,
            text="Examples",
            font=tkinter_font(size=16, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        link_example_frame = CTkFrame(master=right_container_inner_frame)
        link_example_frame.pack(fill="both")
        link_example_inner_frame = CTkFrame(master=link_example_frame)
        link_example_inner_frame.pack(padx=8, fill="both")

        for example_link in EXAMPLE_YOUTUBE_LINKS:
            # truncate text
            truncate_link_text = example_link[:30] + "..."
            CTkButton(
                master=link_example_inner_frame,
                text=truncate_link_text,
                fg_color="transparent",
                anchor="w",
                command=lambda link=example_link: self._link_entry.insert(0, link),
            ).pack(anchor="w", padx=8, fill="x")

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the main window."""
        super().pack(expand=True, fill="both", side="left", anchor="w")

    # Button commands
    def download_youtube_video(self):
        """Download youtube video using the link from entry."""
        # Handling with correct links
        link = self._link_entry.get()
        if not link.startswith("https://"):
            messagebox.showwarning(
                title="Invalid URL", message="Please enter a valid URL."
            )

        # download_youtube_video(link)

    def _on_clip_clicked(self, widget: CTkButton):
        """Handle when clip was clicked.

        Args:
            widget (customtkinter.CTkButton): The widget button of a clip.

        Warning:
            Add error handling when loading a video
            returns error.

        """
        # load image
        vidgen = VidGen()
        clip_path = join("assets/clips/", widget.cget("text"))
        vidgen.load_background_video(clip_path)
        image_bytes = vidgen.get_render_image()
        vidgen.close()
        thumbnail = CTkImage(
            light_image=image_bytes, dark_image=image_bytes, size=(200, 420)
        )
        self._clip_thumbnail_preview.configure(image=thumbnail, text="")
        widget.configure(
            fg_color=ThemeManager.theme["CTkButton"]["fg_color"], hover=False
        )

        if self._previous_selected:
            self._previous_selected.configure(fg_color="transparent", hover=True)

        self._previous_selected = widget

    def _on_delete_clip_clicked(self):
        """Delete the selected clip.

        Notes:
            the previous selected clip can be the current
            clip after it was selected.

        """
        # Don't do anything if none is selected
        if not self._previous_selected:
            return

        clip_path = join("assets/clips/", self._previous_selected.cget("text"))
        remove(clip_path)

        if not isfile(clip_path):
            messagebox.showinfo(title="Success!", message="Video deleted successfully.")
        else:
            messagebox.showerror(
                title="Something went wrong",
                message="Video was not deleted successfully.",
            )

        # return the preview image to default image
        default_image = Image.open("assets/preview/default.png")
        thumbnail = CTkImage(
            light_image=default_image, dark_image=default_image, size=(200, 420)
        )
        self._clip_thumbnail_preview.configure(image=thumbnail, text="Preview")

        # remove the preview previous selected
        self._previous_selected = None

        # reload clips to UI
        self._load_clips_to_ui()

    def _on_download_clip_clicked(self):
        """Download clip from youtube link."""
        # ensure there is a value in the link first
        if not self._link_entry.get():
            messagebox.showerror(title="No Link!", message="Please input a link first!")
            return

        # create a top level window
        download_yt_window = CTkToplevel(self)
        download_yt_window.geometry("400x200")
        download_yt_window.title("Downloading clip")

        # make the window float on LINUX only
        # mainly some of the window managers that needs it.
        if system() == "Linux":
            download_yt_window.attributes("-type", "dialog")

        # ensure always on top
        download_yt_window.attributes("-topmost", True)

        # main container with the widgets information
        main_container = CTkFrame(master=download_yt_window, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=20, pady=20)

        label_container = CTkFrame(master=main_container, fg_color="transparent")
        label_container.pack(expand=True, fill="x")

        # speed
        speed_label = CTkLabel(master=label_container, text="Speed: 0KB")
        speed_label.pack(anchor="w", side="left")

        # download state
        downloaded_label = CTkLabel(master=label_container, text="0MB/0MB")
        downloaded_label.pack(anchor="e")

        # progress bar
        progress_bar = CTkProgressBar(
            master=main_container, mode="determinate", variable=self._progress_variable
        )
        progress_bar.pack(anchor="center", fill="x")
        self._progress_variable.set(value=0)

        close_button = CTkButton(
            master=download_yt_window,
            text="close",
            command=lambda: download_yt_window.destroy(),
            state="disabled",
        )
        close_button.pack(anchor="e", expand=True, padx=20)

        # make sure the behind windows are not interactable
        download_yt_window.after(10, lambda: download_yt_window.grab_set())

        # update the state of the downloading progress
        def progress_hook(status: dict[str, Any]):
            if status.get("status") == "finished":
                # reload clips after download
                self._load_clips_to_ui()

                # enable close button
                close_button.configure(state="normal")

            speed_label.configure(
                text=f"Speed: {human_readable_size(int(status.get('speed', 0)))}"
            )

            # handle estimated or actual total bytes
            total_bytes = int(
                status.get("total_bytes", 0) or status.get("total_bytes_estimate", 0)
            )
            downloaded_bytes = int(status.get("downloaded_bytes", 0))

            # convert sizes to human-readable format
            total_size_str = human_readable_size(total_bytes)
            downloaded_size_str = human_readable_size(downloaded_bytes)

            downloaded_label.configure(text=f"{downloaded_size_str}/{total_size_str}")

            if total_bytes > 0:
                percentage = downloaded_bytes / total_bytes
                self._progress_variable.set(value=percentage)

        # put this into thread because this is a blocking process
        download_thread = threading.Thread(
            target=download_youtube_video, args=(self._link_entry.get(), progress_hook)
        )
        download_thread.start()

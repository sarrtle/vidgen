"""Video section from the sidebar menu.

Shows all the generated videos from the assets/videos
and can delete or upload to social medias.
"""

from os import listdir, remove
from os.path import getmtime, join as pjoin
from platform import system
from threading import Thread
from tkinter import messagebox
from typing import Any, Callable, override
from PIL import Image
from customtkinter import (
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkScrollableFrame,
    CTkToplevel,
    ThemeManager,
)

from models.config_data import ConfigData
from models.upload_model import UploadData
from utility.tools import tkinter_font
from utility.upload import upload_to_facebook
from utility.vidgen_api import VidGen


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

        # important variables
        self._config_data: ConfigData = config_data

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
        self._video_widgets: list[CTkButton] = []
        self._selected_video_path: str | None = None
        self._upload_window: CTkToplevel | None = None

        # important data
        self._uploaded_video: list[str] = []
        self._label_states: list[CTkLabel] = []
        self._description: CTkEntry
        self._hashtags: CTkEntry

        self._platform_data: dict[  # platform type: (token, function)
            str,
            tuple[
                str,
                Callable[
                    [
                        str,
                        ConfigData,
                        UploadData,
                        CTkLabel,
                        Callable[[bool, CTkLabel], None],
                    ],
                    None,
                ],
            ],
        ] = {
            "Facebook": (
                self._config_data.api_settings.facebook_token,
                upload_to_facebook,
            ),
            "Instagram": (
                self._config_data.api_settings.instagram_token,
                upload_to_facebook,
            ),
            "Tiktok": (self._config_data.api_settings.tiktok_token, upload_to_facebook),
            "Youtube": (
                self._config_data.api_settings.youtube_token,
                upload_to_facebook,
            ),
        }

        # setup containers
        self._setup_containers()

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the main window."""
        super().pack(**kwargs)
        # load videos when widget is rendered
        self._load_videos_to_ui()

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
        self._video_list_container.pack(expand=True, fill="both", anchor="w", padx=12)

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
        option_frame.pack(side="left", expand=True, fill="x")

        center_option_frame = CTkFrame(master=option_frame)
        center_option_frame.pack(
            anchor="center", expand=True, fill="x", padx=(0, 220), pady=20
        )

        # Notes:
        #   I am using padx (0, 220) to control the width because
        #   tkinter is so confusing with handling this kind of thing

        self._setup_option_widgets(center_frame=center_option_frame)

        # delete video button
        CTkButton(
            master=option_frame,
            text="Delete",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self._on_video_deleted,
        ).pack(expand=True, fill="x", padx=(0, 220))

    def _setup_option_widgets(self, center_frame: CTkFrame):
        """Set up the options widgets."""
        # main frame for padding
        main_frame = CTkFrame(master=center_frame, fg_color="transparent")
        main_frame.pack(padx=20, pady=20, fill="x", expand=True)

        # Video metadata
        video_metadata_frame = CTkFrame(master=main_frame)
        video_metadata_frame.pack(anchor="w", expand=True, fill="x", pady=(0, 12))

        #   description
        CTkLabel(master=video_metadata_frame, text="Description").pack(anchor="w")
        self._description = CTkEntry(master=video_metadata_frame)
        self._description.pack(anchor="w", fill="x")

        #   hashtags
        hashtag_frame = CTkFrame(master=video_metadata_frame, fg_color="transparent")
        hashtag_frame.pack(expand=True, fill="x")
        CTkLabel(master=hashtag_frame, text="Hashtags").pack(anchor="w")
        self._hashtags = CTkEntry(master=hashtag_frame)
        self._hashtags.pack(fill="x")

        # upload buttons
        upload_frame = CTkFrame(master=main_frame)
        upload_frame.pack(anchor="center", expand=True)

        CTkLabel(master=upload_frame, text="Upload").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        for index, social in enumerate(self._platform_data.keys()):
            row = (index // 2) + 1  # Determine row (integer division)
            col = index % 2  # Determine column (remainder)
            CTkButton(
                master=upload_frame,
                text=social,
                command=lambda platform_type=social: self._on_social_upload_clicked(
                    platform_type
                ),
            ).grid(row=row, column=col, padx=4, pady=4)

    def _load_videos_to_ui(self):
        """Load videos to ui."""
        # remove the current video widgets
        for video_widget in self._video_widgets:
            video_widget.destroy()

        # refresh the video widgets
        video_list = listdir("videos/")

        # sort video by modified time
        video_list.sort(key=lambda video: -getmtime(pjoin("videos/", video)))

        for video in video_list:
            video_path = pjoin("videos/", video)
            video_show_name = video[:5] + "..." + video[65:]
            video_widget = CTkButton(
                master=self._video_list_container,
                text=video_show_name,
                anchor="w",
                fg_color="transparent",
            )
            video_widget.pack(anchor="w", fill="x")
            video_widget.configure(
                command=lambda widget=video_widget, original_path=video_path: self._on_video_clicked(
                    widget, original_path
                )
            )

            # add them to video widgets
            self._video_widgets.append(video_widget)

    # button commands
    def _on_video_clicked(self, widget: CTkButton, original_path: str):
        """Handle when video was clicked.

        Args:
            widget (customtkinter.CTkButton): The widget button of a video.
            original_path (str): The original path of the video

        """
        # don't process on same widget clicked
        if self._previous_selected == widget:
            return

        if self._previous_selected:
            self._previous_selected.configure(fg_color="transparent", hover=True)

        # load image
        vidgen = VidGen()
        vidgen.load_background_video(original_path)
        image_bytes = vidgen.get_render_image()
        vidgen.close()
        thumbnail = CTkImage(
            light_image=image_bytes, dark_image=image_bytes, size=(200, 420)
        )
        self._preview_image_label.configure(image=thumbnail, text="")

        widget.configure(
            fg_color=ThemeManager.theme["CTkButton"]["fg_color"], hover=False
        )

        self._previous_selected = widget
        self._selected_video_path = original_path

    def _on_video_deleted(self):
        """Handle button click for deleting a video."""
        # return if nothing is selected
        if self._previous_selected is None:
            return

        # previous selected can be registered as current selected
        self._previous_selected.destroy()
        self._previous_selected = None

        # delete from local file
        if self._selected_video_path:
            remove(self._selected_video_path)
            self._selected_video_path = None

        # refresh video list
        self._load_videos_to_ui()

    def _on_social_upload_clicked(self, platform_type: str):
        """Handle upload to social media.

        Args:
            platform_type (str): The social media platform type.

        """
        # unpack data
        token, function = self._platform_data[platform_type]

        # check if token is valid
        if not token:
            messagebox.showerror(
                title="Error",
                message=f"Please input your {platform_type} token first.",
            )
            return

        if not self._selected_video_path:
            messagebox.showerror(title="Error", message="Please select a video first.")
            return

        # create top level window for showcasing upload details
        # Label: Uploads
        # Facebook (status):              Uploading (%percentage)
        # Instagram (status):             Uploading (%percentage)
        # Tiktok (status):                Uploading (%percentage)
        # Youtube (status):               Uploading (%percentage)
        label_states = self._setup_upload_toplevel_ui()

        # Don't upload if already uploaded or on process
        if self._selected_video_path in self._uploaded_video:
            return

        # initialize upload data
        upload_data = UploadData(
            description=self._description.get(),
            hashtags=self._hashtags.get(),
        )

        current_label_state = label_states[platform_type.index(platform_type)]
        self._uploaded_video.append(self._selected_video_path)
        thread = Thread(
            target=function,
            args=(
                self._selected_video_path,
                self._config_data,
                upload_data,
                current_label_state,
                self._upload_video_done,
            ),
        )

        thread.start()

    def _setup_upload_toplevel_ui(self) -> list[CTkLabel]:
        """Set up top level window for uploading process."""
        # don't create top level window if already created
        # show it instead
        if self._upload_window:
            self._upload_window.deiconify()
            self._upload_window.grab_set()
            return self._label_states

        # create a top level window
        self._upload_window = CTkToplevel(self)
        self._upload_window.geometry("400x300")
        self._upload_window.title("Uploading video")

        # make the window float on LINUX only
        # mainly some of the window managers that needs it.
        if system() == "Linux":
            self._upload_window.attributes("-type", "dialog")

        # ensure always on top
        self._upload_window.attributes("-topmost", True)

        # main container with the widgets information
        main_container = CTkFrame(master=self._upload_window, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=20, pady=20)

        CTkLabel(
            master=main_container, text="Uploads", font=tkinter_font(16, "bold")
        ).pack(anchor="w")

        social_container = CTkFrame(master=main_container, fg_color="transparent")
        social_container.pack(expand=True, fill="x", pady=(0, 8))

        for social_type in self._platform_data.keys():
            # create a label for each social media
            social_type_frame = CTkFrame(
                master=social_container, fg_color="transparent"
            )
            social_type_frame.pack(expand=True, fill="x", pady=(0, 8))

            CTkLabel(master=social_type_frame, text=f"{social_type} (status):").pack(
                anchor="w", side="left"
            )

            label_state = CTkLabel(master=social_type_frame, text="N/A")
            label_state.pack(anchor="e")
            self._label_states.append(label_state)

        control_container = CTkFrame(master=main_container, fg_color="transparent")
        control_container.pack(expand=True, fill="x")

        # creating a temp variable to fix type checking issue
        upload_window = self._upload_window

        CTkButton(
            master=control_container,
            text="Close",
            command=lambda: [upload_window.grab_release(), upload_window.withdraw()],
        ).pack(anchor="e")

        self._upload_window.after(10, lambda: upload_window.grab_set())

        return self._label_states

    # callback
    def _upload_video_done(
        self,
        status: bool,
        label_state: CTkLabel,
        additional_message: str = "",
        current_video_path_to_upload: str = "",
    ):
        """Call when video upload is done."""
        if not status:
            label_state.configure(
                text=(
                    f"{additional_message} - Failed" if additional_message else "Failed"
                ),
                text_color="#D32F2F",
            )
            self._uploaded_video.remove(current_video_path_to_upload)
        else:
            label_state.configure(text=additional_message, text_color="#4CAF50")

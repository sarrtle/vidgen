"""The Api content section from the sidebar.

Manage API configurations and change AI model.
"""

from tkinter import messagebox
from typing import Any, override
from customtkinter import (
    CTkButton,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkScrollableFrame,
    Variable,
)

from models.config_data import ConfigData
from utility.config_tools import save_api_config
from utility.tools import tkinter_font


class ApiWindow(CTkFrame):
    """Api window contents."""

    def __init__(self, master: CTkFrame, config_data: ConfigData, **kwargs: Any):
        """Initialize Api Window.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            config_data (models.config_data.ConfigData): For saving and loading configurations.
            **kwargs (Any): What CTkFrame needs.

        """
        super().__init__(master, **kwargs)
        self.name: str = "Api"

        # important variables
        self._config_data: ConfigData = config_data

        # save and load values
        self._deepinfra_text_model: Variable = Variable()
        self._deepinfra_vision_model: Variable = Variable()
        self._deepinfra_api_entry: CTkEntry | None = None
        self._openai_text_model: Variable = Variable()
        self._openai_vision_model: Variable = Variable()
        self._openai_api_entry: CTkEntry | None = None
        self._deepgram_api_entry: CTkEntry | None = None

        # main frames
        scrollable_container: CTkScrollableFrame = CTkScrollableFrame(master=self)
        scrollable_container.pack(expand=True, fill="both")
        self._center_container: CTkFrame = CTkFrame(master=scrollable_container)
        self._center_container.pack(anchor="center", expand=True, fill="both", pady=20)

        # initialize widgets and important functions
        self._setup_api_settings_widgets()

    def _setup_api_settings_widgets(self):
        """Set up API settings and widgets.

        Here are the list of widget functions that are
        use to set them up.
        """
        self._setup_deepinfra_settings()
        self._setup_openai_settings()
        self._setup_deepgram_settings()

        # save button
        save_frame = CTkFrame(
            master=self._center_container, fg_color="transparent", width=600, height=30
        )
        save_frame.pack_propagate(False)
        save_frame.pack()
        CTkButton(
            master=save_frame, text="Save", command=self._save_api_settings_to_config
        ).pack(anchor="e")

    def _setup_deepinfra_settings(self):
        """Set up deepinfra settings widgets.

        Notes:
            I created an outer frame called `main_deepinfra_frame`
            and its inner frame called `deepinfra_frame` so that I
            can simulate a beautiful and clean padding of containers
            without hardcoding each widgets for their paddings.

            Turning off pack_propagate seems to make the container
            use the custom widths, if not, no matter how much widths
            we put, the container doesn't follow the widths given.

        Additional Notes:
            Gaps between widgets are 8 pixels.

        """
        main_deepinfra_frame = CTkFrame(self._center_container, width=600, height=180)
        main_deepinfra_frame.pack_propagate(False)
        main_deepinfra_frame.pack(pady=(0, 20))

        deepinfra_frame = CTkFrame(main_deepinfra_frame, fg_color="transparent")
        deepinfra_frame.pack(fill="both", expand=True, padx=20, pady=20)

        CTkLabel(
            master=deepinfra_frame,
            text="DeepInfra",
            font=tkinter_font(size=16, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        choose_model_frame = CTkFrame(deepinfra_frame, fg_color="transparent")
        choose_model_frame.pack(fill="x")
        CTkLabel(
            master=choose_model_frame, text="Text model", font=tkinter_font()
        ).pack(side="left", anchor="w", pady=(0, 8))
        CTkComboBox(
            master=choose_model_frame,
            values=["Llama", "Mixtral"],
            font=tkinter_font(),
            variable=self._deepinfra_text_model,
        ).pack(anchor="e", pady=(0, 8))
        self._deepinfra_text_model.set(
            value=self._config_data.api_settings.deepinfra_text_model
        )

        choose_vision_frame = CTkFrame(deepinfra_frame, fg_color="transparent")
        choose_vision_frame.pack(fill="x")
        CTkLabel(
            master=choose_vision_frame, text="Vision model", font=tkinter_font()
        ).pack(side="left", anchor="w", pady=(0, 8))
        CTkComboBox(
            master=choose_vision_frame,
            values=["Llama-vision-big", "Llama-vision-small"],
            font=tkinter_font(),
            variable=self._deepinfra_vision_model,
        ).pack(anchor="e", pady=(0, 8))
        self._deepinfra_vision_model.set(
            value=self._config_data.api_settings.deepinfra_vision_model
        )

        api_token_frame = CTkFrame(deepinfra_frame, fg_color="transparent")
        api_token_frame.pack(fill="x")
        CTkLabel(master=api_token_frame, text="Api Token", font=tkinter_font()).pack(
            side="left", anchor="w"
        )
        self._deepinfra_api_entry = CTkEntry(
            master=api_token_frame,
            placeholder_text="aZQNwiXQ*****",
        )
        self._deepinfra_api_entry.pack(anchor="e")

        if self._config_data.api_settings.deepinfra_token:
            self._deepinfra_api_entry.insert(
                0, self._config_data.api_settings.deepinfra_token
            )

    def _setup_openai_settings(self):
        """Set up openai settings widgets."""
        main_openai_frame = CTkFrame(self._center_container, width=600, height=180)
        main_openai_frame.pack_propagate(False)
        main_openai_frame.pack(pady=(0, 20))

        openai_frame = CTkFrame(main_openai_frame, fg_color="transparent")
        openai_frame.pack(fill="both", expand=True, padx=20, pady=20)

        CTkLabel(
            master=openai_frame,
            text="Openai",
            font=tkinter_font(size=16, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        choose_model_frame = CTkFrame(openai_frame, fg_color="transparent")
        choose_model_frame.pack(fill="x")
        CTkLabel(
            master=choose_model_frame, text="Text model", font=tkinter_font()
        ).pack(side="left", anchor="w", pady=(0, 8))
        CTkComboBox(
            master=choose_model_frame,
            values=["Gpt-4o", "Gpt-4o-mini"],
            font=tkinter_font(),
            variable=self._openai_text_model,
        ).pack(anchor="e", pady=(0, 8))
        self._openai_text_model.set(
            value=self._config_data.api_settings.openai_text_model
        )

        choose_vision_frame = CTkFrame(openai_frame, fg_color="transparent")
        choose_vision_frame.pack(fill="x")
        CTkLabel(
            master=choose_vision_frame, text="Vision model", font=tkinter_font()
        ).pack(side="left", anchor="w", pady=(0, 8))
        CTkComboBox(
            master=choose_vision_frame,
            values=["Gpt-4o", "Gpt-4o-mini"],
            font=tkinter_font(),
            variable=self._openai_vision_model,
        ).pack(anchor="e", pady=(0, 8))
        self._openai_vision_model.set(
            value=self._config_data.api_settings.openai_vision_model
        )

        api_token_frame = CTkFrame(openai_frame, fg_color="transparent")
        api_token_frame.pack(fill="x")
        CTkLabel(master=api_token_frame, text="Api Token", font=tkinter_font()).pack(
            side="left", anchor="w"
        )
        self._openai_api_entry = CTkEntry(
            master=api_token_frame,
            placeholder_text="sk-********",
        )
        self._openai_api_entry.pack(anchor="e")

        if self._config_data.api_settings.openai_token:
            self._openai_api_entry.insert(
                0, self._config_data.api_settings.openai_token
            )

    def _setup_deepgram_settings(self):
        """Set up Deepgram settings widgets."""
        main_deepgram_frame = CTkFrame(
            master=self._center_container, width=600, height=110
        )
        main_deepgram_frame.pack_propagate(False)
        main_deepgram_frame.pack(pady=(0, 12))

        deepgram_frame = CTkFrame(master=main_deepgram_frame, fg_color="transparent")
        deepgram_frame.pack(fill="both", expand=True, padx=20, pady=20)

        CTkLabel(
            master=deepgram_frame,
            text="Deepgram",
            font=tkinter_font(size=16, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        api_token_frame = CTkFrame(deepgram_frame, fg_color="transparent")
        api_token_frame.pack(fill="x")
        CTkLabel(master=api_token_frame, text="Api token", font=tkinter_font()).pack(
            side="left", anchor="w"
        )
        self._deepgram_api_entry = CTkEntry(
            master=api_token_frame,
            placeholder_text="bARMxmYR*****",
        )
        self._deepgram_api_entry.pack(anchor="e")

        if self._config_data.api_settings.deepgram_token:
            self._deepgram_api_entry.insert(
                0, self._config_data.api_settings.deepgram_token
            )

    def _get_entry_values(self, entry: CTkEntry | None) -> str | None:
        """Dynamically get the values from text entry widgets.

        Args:
            entry (customtkinter.CTkEntry): The entry widget.

        Returns:
            str | None: The value of the entry widget otherwise None

        """
        if entry is not None:
            return entry.get()
        return None

    def _save_api_settings_to_config(self):
        """Save API settings to `config.json` local file."""
        # save all values
        self._config_data.api_settings.deepinfra_text_model = (
            self._deepinfra_text_model.get()
        )
        self._config_data.api_settings.deepinfra_vision_model = (
            self._deepinfra_vision_model.get()
        )
        self._config_data.api_settings.deepinfra_token = self._get_entry_values(
            self._deepinfra_api_entry
        )

        self._config_data.api_settings.openai_text_model = self._openai_text_model.get()
        self._config_data.api_settings.openai_vision_model = (
            self._openai_vision_model.get()
        )
        self._config_data.api_settings.openai_token = self._get_entry_values(
            self._openai_api_entry
        )

        self._config_data.api_settings.deepgram_token = self._get_entry_values(
            self._deepgram_api_entry
        )

        save_api_config(config_object=self._config_data)
        messagebox.showinfo(title="Success", message="Settings has been saved!")

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the main window."""
        super().pack(expand=True, fill="both", side="left", anchor="w")

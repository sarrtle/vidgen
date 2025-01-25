"""The sidebar content of story section from the sidebar."""

from os.path import isfile
from platform import system
from tkinter import messagebox, filedialog
from typing import Any, override
from threading import Thread

from PIL import Image
from customtkinter import (
    CTkButton,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkProgressBar,
    CTkScrollableFrame,
    CTkSlider,
    CTkTextbox,
    CTkToplevel,
    IntVar,
    Variable,
)

from utility.generate_text import GenerateText
from utility.generate_voice import GenerateVoice
from utility.render_story import RenderStory
from utility.tools import create_audio_filename, play_voiceover, tkinter_font
from utility.vidgen_api import VidGen
from models.config_data import ConfigData
from models.story_window_model import StoryWindowValues
from utility.config_tools import save_api_config


class StoryWindow(CTkFrame):
    """Story window contents."""

    def __init__(self, master: CTkFrame, config_data: ConfigData, **kwargs: Any):
        """Initialize story window.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            config_data (models.config_data.ConfigData): For saving and loading configurations
            **kwargs (Any): What CTkFrame needs.

        Notes:
            This component has 2 containers. The left one is
            the preview image and the right one is the video
            settings.

        """
        super().__init__(master, **kwargs)
        self.name: str = "Story"

        # important variables
        self._config_data: ConfigData = config_data
        self._story_widows_values: StoryWindowValues | None = None
        self._clip_path: str | None = None
        self._video_file_clip: VidGen = VidGen()
        self._stroke_label: CTkLabel
        self._stroke_save_schedule: str | None = None

        # values get and set
        self._theme_variable: Variable = Variable(value="Horror")
        self._text_model_variable: Variable = Variable(value="DeepInfra")
        self._idea_entry: CTkEntry
        self._context_textbox: CTkTextbox
        self._voice_model_variable: Variable = Variable(value="aura-arcas-en")
        self._text_font_variable: Variable = Variable(value="default")
        self._text_color_variable: Variable = Variable(value="yellow")
        self._text_style_variable: Variable = Variable(value="3 words")
        self._text_stroke_variable: IntVar = IntVar(value=5)

        # left and right container
        self._left_side_container: CTkFrame
        self._right_side_container: CTkFrame

        # image preview widget
        self._image_preview_widget: CTkLabel

        # control widgets
        self._generate_idea_button: CTkButton
        self._render_progress_variable: Variable = Variable(value=0)
        self._progress_label_indicator: CTkLabel
        self._render_close_button: CTkButton

        # setup important functions
        self._setup_containers()

    def _setup_containers(self):
        """Set up the preview and control options for Story window."""
        self._left_side_container = CTkFrame(master=self)
        self._left_side_container.pack(fill="both", side="left")
        scrollable_right_side_container = CTkScrollableFrame(
            master=self, fg_color="transparent"
        )
        scrollable_right_side_container.pack(fill="both", expand=True)
        self._right_side_container = CTkFrame(
            master=scrollable_right_side_container, fg_color="transparent"
        )
        self._right_side_container.pack(
            fill="both", expand=True, padx=24, pady=(24, 16)
        )

        CTkButton(master=self, text="Render Video", command=self._on_render_video).pack(
            anchor="e", padx=24, pady=(8, 16)
        )

        # load image preview
        default_image = Image.open("assets/preview/default.png")
        self._image_preview_widget = CTkLabel(
            master=self._left_side_container,
            text="Preview",
            image=CTkImage(
                light_image=default_image, dark_image=default_image, size=(360, 640)
            ),
        )
        self._image_preview_widget.pack(anchor="center", expand=True, padx=32)

        self._setup_settings_and_options()

    def _setup_settings_and_options(self):
        """Set up settings and options.

        Here are the list of widget functions that are
        use to set them up.
        """
        self._setup_theme_text_model()
        self._setup_idea_context_settings()
        self._setup_preview_voiceover_settings()
        self._setup_video_options_settings()

    def _setup_theme_text_model(self):
        """Set up theme and text model widgets."""
        # Theme
        theme_text_model_frame = CTkFrame(master=self._right_side_container)
        theme_text_model_frame.pack(fill="x", expand=True)
        theme_frame = CTkFrame(master=theme_text_model_frame, fg_color="transparent")
        theme_frame.pack(fill="x", expand=True)
        CTkLabel(master=theme_frame, text="Theme", font=tkinter_font(16, "bold")).pack(
            side="left", anchor="w", padx=16, pady=16
        )
        CTkComboBox(
            master=theme_frame,
            values=["Horror", "Facts"],
            variable=self._theme_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=16)
        self._theme_variable.set(value=self._config_data.story_settings.theme)

        # AI model
        # use theme text model frame since they are group
        ai_model_frame = CTkFrame(master=theme_text_model_frame, fg_color="transparent")
        ai_model_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=ai_model_frame, text="Text Model", font=tkinter_font(16, "bold")
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=ai_model_frame,
            values=["DeepInfra", "Openai", "Gemini"],
            variable=self._text_model_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_model_variable.set(value=self._config_data.story_settings.text_model)

    def _setup_idea_context_settings(self):
        """Set up generate from idea and edit context widgets."""
        # Idea
        idea_context_frame = CTkFrame(master=self._right_side_container)
        idea_context_frame.pack(fill="x", expand=True, pady=20)
        idea_frame = CTkFrame(master=idea_context_frame, fg_color="transparent")
        idea_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=idea_frame,
            text="Idea",
            font=tkinter_font(16, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 8))
        self._idea_entry = CTkEntry(
            master=idea_context_frame,
            placeholder_text="Tell me your idea.",
        )
        self._idea_entry.pack(fill="x", padx=16, pady=(0, 8))
        self._generate_idea_button = CTkButton(
            master=idea_context_frame, text="Generate", command=self._on_generate_idea
        )
        self._generate_idea_button.pack(anchor="e", padx=16, pady=(0, 8))

        # Context
        CTkLabel(
            master=idea_context_frame, text="Context", font=tkinter_font(16, "bold")
        ).pack(anchor="w", padx=16)
        CTkLabel(
            master=idea_context_frame,
            text="Paste if you have an already made content or feel free to edit from the generated idea.",
            font=tkinter_font(12, "normal"),
        ).pack(anchor="w", padx=16, pady=(0, 8))
        self._context_textbox = CTkTextbox(master=idea_context_frame)
        self._context_textbox.pack(fill="x", padx=16, pady=(0, 16))

    def _setup_preview_voiceover_settings(self):
        """Set up preview voiceover widgets."""
        # Preview voiceover
        preview_voiceover_frame = CTkFrame(master=self._right_side_container)
        preview_voiceover_frame.pack(fill="x", expand=True, pady=(0, 20))
        voice_model_frame = CTkFrame(preview_voiceover_frame, fg_color="transparent")
        voice_model_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=voice_model_frame,
            text="Voice model",
            font=tkinter_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=16)
        CTkComboBox(
            master=voice_model_frame,
            values=["aura-arcas-en", "aura-luna-en", "aura-asteria-en"],
            font=tkinter_font(),
            variable=self._voice_model_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(16, 0))
        self._voice_model_variable.set(
            value=self._config_data.story_settings.voice_model
        )
        CTkButton(
            master=voice_model_frame, text="Play", command=self._on_voiceover_play
        ).pack(anchor="e", padx=16, pady=(8, 16))

    def _setup_video_options_settings(self):
        """Set up video options widgets."""
        # video options
        video_options_frame = CTkFrame(master=self._right_side_container)
        video_options_frame.pack(fill="x", expand=True)

        # clips
        clips_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        clips_frame.pack(fill="x", expand=True)
        CTkLabel(master=clips_frame, text="Clips", font=tkinter_font(16, "bold")).pack(
            anchor="w", side="left", padx=16, pady=16
        )
        CTkButton(
            master=clips_frame, text="browse", command=self._on_browse_files
        ).pack(anchor="e", padx=16, pady=16)

        # randomize position
        randomize_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        randomize_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=randomize_frame,
            text="Randomize position",
            font=tkinter_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkButton(master=randomize_frame, text="randomize").pack(
            anchor="e", padx=16, pady=(0, 16)
        )

        # text font
        text_font_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        text_font_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=text_font_frame,
            text="Text font",
            font=tkinter_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=text_font_frame,
            values=["default", "Futura", "Monosans"],
            font=tkinter_font(),
            variable=self._text_font_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_font_variable.set(value=self._config_data.story_settings.font)

        # text color
        text_color_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        text_color_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=text_color_frame, text="Text color", font=tkinter_font(16, "bold")
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=text_color_frame,
            values=["white", "yellow", "violet", "blue"],
            font=tkinter_font(),
            variable=self._text_color_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_color_variable.set(value=self._config_data.story_settings.text_color)

        # text style
        text_style_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        text_style_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=text_style_frame, text="Text style", font=tkinter_font(16, "bold")
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=text_style_frame,
            values=["1 word", "3 words"],
            variable=self._text_style_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_style_variable.set(value=self._config_data.story_settings.text_style)

        # text stroke width
        text_stroke_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        text_stroke_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=text_stroke_frame, text="Text stroke", font=tkinter_font(16, "bold")
        ).pack(side="left", anchor="w", padx=(16, 0), pady=(0, 16))
        stroke_slider_frame = CTkFrame(master=text_stroke_frame)
        stroke_slider_frame.pack(anchor="e", padx=16, pady=(0, 16))
        self._stroke_label = CTkLabel(
            master=stroke_slider_frame,
            text=str(self._config_data.story_settings.text_stroke),
            font=tkinter_font(),
        )
        self._stroke_label.pack(side="left", padx=8, anchor="w")
        CTkSlider(
            master=stroke_slider_frame,
            number_of_steps=10,
            from_=1,
            to=10,
            orientation="horizontal",
            width=120,
            variable=self._text_stroke_variable,
            command=lambda _: self._on_text_stroke_slider_event(),
        ).pack(anchor="e", pady=8)
        self._text_stroke_variable.set(
            value=self._config_data.story_settings.text_stroke
        )

    def _get_idea_entry_value(self):
        """Get the value of entry from idea entry."""
        if self._idea_entry:
            return self._idea_entry.get()

        return ""

    def _get_context_textbox_value(self):
        """Get the valuue of text box from context."""
        if self._context_textbox:
            return self._context_textbox.get("1.0", "end-1c")

        return ""

    def _get_all_values(self):
        """Get all values from the story window settings."""
        return StoryWindowValues(
            theme=self._theme_variable.get(),
            text_model=self._text_model_variable.get(),
            idea=self._get_idea_entry_value(),
            context=self._get_context_textbox_value(),
            voice_model=self._voice_model_variable.get(),
            text_font=self._text_font_variable.get(),
            text_color=self._text_color_variable.get(),
            text_style=self._text_style_variable.get(),
            text_stroke=self._text_stroke_variable.get(),
        )

    def _save_story_settings_to_config(self):
        """Save story settings to `config.json` local file."""
        story_windows_values = self._get_all_values()

        # save story settings data on config
        self._config_data.story_settings.theme = story_windows_values.theme
        self._config_data.story_settings.text_model = story_windows_values.text_model
        self._config_data.story_settings.voice_model = story_windows_values.voice_model
        self._config_data.story_settings.font = story_windows_values.text_font
        self._config_data.story_settings.text_color = story_windows_values.text_color
        self._config_data.story_settings.text_style = story_windows_values.text_style
        self._config_data.story_settings.text_stroke = story_windows_values.text_stroke

        save_api_config(config_object=self._config_data)

    def _load_preview_image(self, image: Image.Image):
        """Load the image inside the preview widget.

        Args:
            image (Image.Image): Loaded pillow image.

        Raises:
            AssertionError: if only the image preview widget is None.

        """
        assert (
            self._image_preview_widget is not None
        ), "Something unexpected happen, image preview widget was not loaded."

        self._image_preview_widget.configure(
            text="",
            image=CTkImage(light_image=image, dark_image=image, size=(360, 640)),
        )

    # Button commands
    def _on_generate_idea(self):
        """Generate context base on idea."""
        idea_string = self._get_idea_entry_value()

        # Show warning if no idea input
        if not idea_string:
            messagebox.showwarning(
                title="No Idea!",
                message="Please input some idea before clicking generate.",
            )
            return

        # disable the button
        self._generate_idea_button.configure(state="disabled")

        # initialize generate text
        generate_text = GenerateText(
            idea=idea_string,
            config_object=self._config_data,
            done_callback=self._on_done_generate_idea,
        )
        thread = Thread(target=generate_text.request)
        thread.start()

    def _on_browse_files(self):
        """Browse all clips inside the assets folder."""
        # load (1) clip for now
        clip = filedialog.askopenfilename(
            defaultextension=".mp4", initialdir="assets/clips/"
        )

        if not clip:
            return

        self._clip_path = clip
        self._video_file_clip.load_background_video(self._clip_path)

        # load image preview
        image = self._video_file_clip.get_render_image()
        self._load_preview_image(image=image)

    def _on_voiceover_play(self):
        """Generate and play voiceover sample."""
        # check deepgram valid token
        if not self._config_data.api_settings.deepgram_token:
            messagebox.showerror(
                title="No deepgram token!",
                message="Please input deepgram API token first.",
            )
            return

        # get the script context
        script_context = self._context_textbox.get("1.0", "end").strip()
        if not script_context:
            messagebox.showerror(
                title="Error",
                message="Please input your story context first or generate from idea.",
            )
            return

        filename = create_audio_filename(
            script=script_context,
            voice_model_name=self._config_data.story_settings.voice_model,
        )

        # check if audio is already generated
        is_voice_generated = True
        if not isfile(filename):
            # generate an audio
            generate_voice = GenerateVoice(
                script=script_context, config_data=self._config_data
            )
            is_voice_generated = generate_voice.generate()
        if is_voice_generated:
            play_voiceover(filepath=filename)

    def _on_render_video(self):
        """Render video from story settings."""
        # get the script context and
        # check script content if empty for validation
        script_context = self._context_textbox.get("1.0", "end").strip()
        if not script_context:
            messagebox.showerror(
                title="Error",
                message="Please input your story context first or generate from idea.",
            )
            return

        # check if clip loaded
        if not self._video_file_clip.is_background_video_loaded():
            messagebox.showerror(
                title="Error",
                message="Please load a background video first.",
            )
            return

        # create a top level window
        render_video_window = CTkToplevel(self)
        render_video_window.geometry("400x130")
        render_video_window.title("Rendering video")

        # make the window float on LINUX
        # mainly some of the window managers that needs it
        if system() == "Linux":
            render_video_window.attributes("-type", "dialog")

        # ensure always on top
        render_video_window.attributes("-topmost", True)

        # main container
        main_container = CTkFrame(master=render_video_window, fg_color="transparent")
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        filepath = "Rendering video - "
        filepath_label = CTkLabel(
            master=main_container,
            text=filepath,
            font=tkinter_font(weight="bold"),
        )
        filepath_label.pack(anchor="w")

        # progress bar
        progress_frame = CTkFrame(master=main_container, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 4))
        progress_bar = CTkProgressBar(
            master=progress_frame,
            mode="determinate",
            variable=self._render_progress_variable,
        )
        progress_bar.pack(anchor="w", fill="x", side="left", expand=True)
        self._progress_label_indicator = CTkLabel(master=progress_frame, text="0/?")
        self._progress_label_indicator.pack()

        # I need to pass the _render_progress_variable and
        # _progress_label_indicator to the callback logger

        self._render_close_button = CTkButton(
            master=main_container,
            text="Close",
            state="disabled",
            command=lambda: render_video_window.destroy(),
        )
        self._render_close_button.pack(anchor="se")

        # make sure the behind windows are not interactable
        render_video_window.after(10, lambda: render_video_window.grab_set())

        # render moviepy on thread here
        render_story = RenderStory(
            script=script_context,
            config_data=self._config_data,
            vidgen_object=self._video_file_clip,
            progress_bar_variable=self._render_progress_variable,
            progress_label_variable=self._progress_label_indicator,
            done_callback=self.on_done_rendering_video,
        )

        # get filename and update label
        filename = self._video_file_clip.get_video_filepath()
        filepath_label.configure(text=f"Rendering video - {filename[:20]}...")

        # render on thread
        # check if config is 3 word or 1 word
        if self._config_data.story_settings.text_style == "3 words":
            thread = Thread(target=render_story.render_three_words)
        elif self._config_data.story_settings.text_style == "1 word":
            thread = Thread(target=render_story.render_one_word)
        # default
        else:
            thread = Thread(target=render_story.render_three_words)
        thread.start()

    # events
    def _on_text_stroke_slider_event(self):
        """Text stroke slider event handler."""
        self._stroke_label.configure(text=str(self._text_stroke_variable.get()))

        if self._stroke_save_schedule is not None:
            self.after_cancel(self._stroke_save_schedule)

        # schedule a save operation after 300 ms when sliding was not used.
        self._stroke_save_schedule = self.after(
            ms=300, func=self._save_story_settings_to_config
        )

    # callbacks
    def _on_done_generate_idea(
        self,
        generated_text: str,
        error: bool,
        error_title: str | None,
        error_message: str | None,
    ):
        """Will call this function after completing the thread process.

        Args:
            generated_text (str): The generated text from AI API service.
            error (bool): Indicates if error occurs.
            error_title (str | None): The title of the error to show.
            error_message (str | None): The message of the errorto show.

        """
        # enable the generate idea button again
        self._generate_idea_button.configure(state="normal")

        if error:
            messagebox.showerror(title=error_title, message=error_message)
            return

        # update the textbox with newly generated text
        self._context_textbox.delete("1.0", "end")
        self._context_textbox.insert("1.0", generated_text)

    def on_done_rendering_video(self):
        """Call this function when rendering the video is done."""
        self._render_close_button.configure(state="normal")

    @override
    def pack(self, **kwargs: Any):
        """Render the component to the main window."""
        super().pack(expand=True, fill="both", side="left", anchor="w")

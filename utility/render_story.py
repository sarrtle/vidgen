"""Module for rendering the story video."""

from tkinter import Variable
from typing import Any, Callable
from PIL import Image
from PIL.ImageFont import FreeTypeFont
from customtkinter import CTkLabel
from moviepy import AudioFileClip, TextClip
from moviepy.video.VideoClip import ImageDraw
from models.config_data import ConfigData
from utility.custom_render_logger import CustomMoviepyLogger
from utility.generate_voice import GenerateVoice
from utility.tools import create_audio_filename
from utility.vidgen_api import VidGen


class RenderStory:
    """RenderStory object."""

    def __init__(
        self,
        script: str,
        config_data: ConfigData,
        vidgen_object: VidGen,
        progress_bar_variable: Variable,
        progress_label_variable: CTkLabel,
        done_callback: Callable[[], None],
    ):
        """Initialize RenderStory.

        Args:
            script (str): The generated or pasted script context story.
            config_data (models.ConfigData): The project configurations.
            vidgen_object (utility.Vidgen): The initialized Vidgen object.
            progress_bar_variable (Variable): The progress bar variable.
            progress_label_variable (CTkLabel): The progress label variable.
            done_callback (Callable[[], None]): The callback function when done.

        """
        self._script: str = script
        self._config_data: ConfigData = config_data
        self._vidgen_object: VidGen = vidgen_object
        self._progress_bar_variable: Variable = progress_bar_variable
        self._progress_label_variable: CTkLabel = progress_label_variable
        self._done_callback: Callable[[], None] = done_callback

        # get audio transcription data
        generate_voice_object = GenerateVoice(
            script=self._script, config_data=self._config_data
        )
        audio_transcription_data = generate_voice_object.transcript()
        self._word_data: list[Any] = audio_transcription_data["results"]["channels"][0][
            "alternatives"
        ][0]["words"]

        # unpack vidgen parameters
        self._video_width: int = self._vidgen_object.video_width
        self._video_height: int = self._vidgen_object.video_height
        self.x_center: float = self._vidgen_object.center_position_x
        self.y_center: float = self._vidgen_object.center_position_y
        self._font: str = self._vidgen_object.font
        self._font_object: FreeTypeFont = self._vidgen_object.font_object

    def render_three_words(self):
        """Render the video on one three words style format."""
        # construct a word data of 3 words
        # get data: overall duration, startime and endtime
        chunked_word_data = []
        for i in range(0, len(self._word_data), 3):
            # chunk into 3 words
            chunked_words_data = self._word_data[i : i + 3]
            chunked_words = [w.get("punctuated_word") for w in chunked_words_data]
            # start time of each word from 3 chunked words
            word_start_time_data = [w["start"] for w in chunked_words_data]
            # end time of each word from chunked words
            word_end_time_data = [w["end"] for w in chunked_words_data]
            # overall duration of 3 chunked words
            overall_duration = sum(
                [w.get("end") - w.get("start") for w in chunked_words_data]
            )

            chunked_word_data.append(
                {
                    "words": chunked_words,
                    "start_time": word_start_time_data,
                    "end_time": word_end_time_data,
                    "overall_duration": overall_duration,
                }
            )

        # create a sample image object for text calculation
        image = Image.new(
            "RGB",
            (self._video_width, self._video_height),
            "black",
        )
        draw = ImageDraw.Draw(image)

        # the space of the word, matters
        space_size = self._font_object.getlength(" ")

        # work for the 3 words
        word_clips = []
        word_highlighted_clips = []
        for word_data in chunked_word_data:
            # overall_duration, start_time, words, end_time
            chunked_words = word_data["words"]
            overall_duration = word_data["overall_duration"]

            # ====== calculate position =====
            overall_width = sum(
                [self._font_object.getlength(w) + space_size for w in chunked_words]
            )
            # don't include the last space on last word
            overall_width -= space_size

            # check if the overall width overlaps with the maximum width of the video
            # padding is set for something like a margine for hte whole video screen
            padding = 100
            is_overlap = (padding + overall_width) - self._video_width > 0

            # if overlap, we will remove the last word, and put it at the second
            # line, these varialbes will be use outside the overlap condition
            second_line_starting_x_position = 0
            second_line_y_position = 0
            line_spacing = 30
            last_word_height = 0

            if is_overlap:
                # get the height of the last word to properly center them on the second line
                bbox = draw.textbbox((0, 0), chunked_words[-1], font=self._font_object)
                last_word_height = bbox[3] - bbox[1]

                # remove the last word from the overall_width, so the first line words will
                # have their own original center position later when calculated on starting_x_position
                last_word_width = self._font_object.getlength(chunked_words[-1])
                overall_width -= last_word_width

                # calculate the second line starting x posistion
                second_line_starting_x_position = self._x_center - (
                    last_word_width // 2
                )
                # calculate the second line y position with line spacing of 30 between first and second line
                second_line_y_position = self._y_center + (
                    (last_word_height + line_spacing) // 2
                )

            # create the first line starting x position
            starting_x_position = self._x_center - (overall_width // 2)

            # base layer of the 3 words, no highlights
            word_clip_data = []
            # previous word width will be use to calculate the next starting x position plus space size
            previous_word_width = 0
            for word_index, word in enumerate(chunked_words):
                word_clip = TextClip(
                    text=word,
                    color="white",
                    font=self._font,
                    font_size=self._vidgen_object.font_size,
                    stroke_width=self._config_data.story_settings.text_stroke,
                    stroke_color="black",
                )

                # set their respective positions
                word_clip = word_clip.with_position((starting_x_position, "center"))
                # notice that I am using their original start time and end time
                # for overall duration
                word_clip = word_clip.with_start(word_data["start_time"][0])
                word_clip = word_clip.with_end(word_data["end_time"][-1])

                # change the last word y position if overlap
                if is_overlap:
                    # last word will have their special place on second linee
                    if word_index == len(chunked_words) - 1:
                        word_clip = word_clip.with_position(
                            (second_line_starting_x_position, second_line_y_position)
                        )
                    # change the first line y position to match the second line height
                    else:
                        word_clip = word_clip.with_position(
                            (
                                starting_x_position,
                                "center",
                            )
                        )

                # save the base word clip
                word_clips.append(word_clip)

                # save the word clip data for highlighting text clips
                word_clip_data.append(
                    {
                        "word": word,
                        "position": (
                            [starting_x_position, "center"]
                            if not is_overlap
                            else (
                                [
                                    second_line_starting_x_position,
                                    second_line_y_position,
                                ]
                                if word_index == len(chunked_words) - 1
                                else [starting_x_position, "center"]
                            )
                        ),
                        # The start time and end time in here will use the highlighted
                        # current word that the speaker is speaking,
                        "start_time": word_data["start_time"][word_index],
                        "end_time": word_data["end_time"][word_index],
                    }
                )

                # save the current word width for the next starting x position
                previous_word_width = self._font_object.getlength(word) + space_size

                # update the starting x position
                starting_x_position += previous_word_width

            # highlight the words
            for word_highlight_data in word_clip_data:
                word_highlighted_clip = TextClip(
                    text=word_highlight_data["word"],
                    color=self._config_data.story_settings.text_color,
                    font=self._font,
                    font_size=self._vidgen_object.font_size,
                    stroke_width=self._config_data.story_settings.text_stroke,
                    stroke_color="black",
                )

                # set their respective positions
                word_highlighted_clip = word_highlighted_clip.with_position(
                    word_highlight_data["position"]
                )

                # notice that I am using their original start time and end time
                # for overall duration
                word_highlighted_clip = word_highlighted_clip.with_start(
                    word_highlight_data["start_time"]
                )
                word_highlighted_clip = word_highlighted_clip.with_end(
                    word_highlight_data["end_time"]
                )

                word_highlighted_clips.append(word_highlighted_clip)

        # add the clips to the vidgen object
        self._vidgen_object.add_text_clip(word_clips)
        self._vidgen_object.add_text_clip(word_highlighted_clips)

        # load the audio voiceover
        voiceover_path = create_audio_filename(
            script=self._script,
            voice_model_name=self._config_data.story_settings.voice_model,
        )
        self._vidgen_object.add_audio(AudioFileClip(voiceover_path))

        # assuming everything is done above
        self._vidgen_object.render(
            custom_callback=CustomMoviepyLogger(
                progress_bar_variable=self._progress_bar_variable,
                progress_label_variable=self._progress_label_variable,
            )
        )

        # call the down callback from the user interface
        self._done_callback()

    def render_one_word(self):
        """Render the video on one word style format."""
        word_clips = []
        for wd in self._word_data:
            word_clip = TextClip(
                text=wd["word"],
                color=self._config_data.story_settings.text_color,
                font=self._font,
                font_size=self._vidgen_object.font_size,
                stroke_width=self._config_data.story_settings.text_stroke,
                stroke_color="black",
            )

            # set their respective positions
            word_clip = word_clip.with_position(("center", "center"))

            # notice that I am using their original start time and end time
            # for overall duration
            word_clip = word_clip.with_start(wd["start"])
            word_clip = word_clip.with_end(wd["end"])

            word_clips.append(word_clip)

        # add the clips to the vidgen object
        self._vidgen_object.add_text_clip(word_clips)

        # load the audio voiceover
        voiceover_path = create_audio_filename(
            script=self._script,
            voice_model_name=self._config_data.story_settings.voice_model,
        )
        self._vidgen_object.add_audio(AudioFileClip(voiceover_path))

        # assuming everything is done above
        self._vidgen_object.render(
            custom_callback=CustomMoviepyLogger(
                progress_bar_variable=self._progress_bar_variable,
                progress_label_variable=self._progress_label_variable,
            )
        )

        # call the down callback from the user interface
        self._done_callback()

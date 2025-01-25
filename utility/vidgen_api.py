"""All API for generating the video."""

from os import mkdir
from os.path import isdir
from PIL import ImageFont, Image
from moviepy import (
    AudioClip,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
)

from exceptions.vid_gen_exceptions import NoVideoFileCLip
from utility.custom_render_logger import CustomMoviepyLogger
from utility.tools import create_video_filename


class VidGen:
    """The object to reuse and edit the video before rendering.

    Attributes:
        video_width (int): The width of the video.
        video_height (int): The height of the video.
        center_position_x (float): The x position of the text.
        center_position_y (float): The y position of the text.
        font_size (int): The font size of the text.
        font (str): The font path of the text.
        font_object (ImageFont.FreeTypeFont): The font object of the text.

    Methods:
        load_video: Lazily load the video into moviepy.
        load_font: Load font to be use in the video.
        get_render_image: Get a rendered image form the video and text.

    """

    def __init__(self):
        """Initialize Vidgen.

        Args:
            video_file_path (str): The filepath of the video.

        """
        # video properties
        self._video_file_clip: VideoFileClip | None = None
        self.video_height: int = 1920
        self.video_width: int = 1080

        # text positioning
        self.center_position_x: float = self.video_width // 2
        self.center_position_y: float = self.video_height // 2

        # text manipulation
        self.font_size: int = 80
        self.font: str = self.load_font()
        self.font_object: ImageFont.FreeTypeFont = ImageFont.truetype(
            font=self.font, size=self.font_size
        )

        # clips
        self._text_clips: list[TextClip] = []
        self._audio_clips: list[AudioClip] = []
        self._image_clips: list[ImageClip] = []

    def load_background_video(self, filepath: str):
        """Lazily Load the video into moviepy.

        Args:
            filepath (str): The filepath of the video.

        """
        self._video_file_clip = VideoFileClip(filepath)

    def is_background_video_loaded(self) -> bool:
        """Check if the video is loaded."""
        return self._video_file_clip is not None

    def load_font(self, default: bool = True, filepath: str | None = None) -> str:
        """Load font to be use in the video."""
        default_font = "assets/fonts/futura-extra-bold.ttf"

        if default:
            return default_font

        if filepath is None:
            return default_font

        return filepath

    def get_render_image(self) -> Image.Image:
        """Get a rendered image from the video and text.

        Get an image from the video and turn them as a Pillow Image object.

        Raises:
            NoVideoFileCLip: If there was no video loaded yet.

        """
        if not self._video_file_clip:
            raise NoVideoFileCLip

        seconds = 2
        frame = self._video_file_clip.get_frame(
            seconds
        )  # returns np array but this is Any

        image = Image.fromarray(frame)

        return image

    def add_text_clip(self, text_clip: TextClip | list[TextClip]) -> None:
        """Add text clip to Vidgen.

        Notes:
            Ensure the text clip is already finalized and
            edited before adding to Vidgen.

        """
        (
            self._text_clips.append(text_clip)
            if isinstance(text_clip, TextClip)
            else self._text_clips.extend(text_clip)
        )

    def add_audio(self, audio_clip: AudioFileClip | list[AudioFileClip]) -> None:
        """Add audio clip to Vidgen.

        Notes:
            Ensure the audio clip is already finalized and
            edited before adding to Vidgen.

        """
        (
            self._audio_clips.append(audio_clip)
            if isinstance(audio_clip, AudioClip)
            else self._audio_clips.extend(audio_clip)
        )

    def add_image_clip(self, image_clip: ImageClip | list[ImageClip]) -> None:
        """Add image clip to Vidgen.

        Notes:
            Ensure the image clip is already finalized and
            edited before adding to Vidgen.

        """
        (
            self._image_clips.append(image_clip)
            if isinstance(image_clip, ImageClip)
            else self._image_clips.extend(image_clip)
        )

    def get_video_filepath(self) -> str:
        """Get video filepath."""
        return (
            create_video_filename(self._video_file_clip.filename)
            if self._video_file_clip
            else ""
        )

    def render(self, custom_callback: CustomMoviepyLogger) -> None:
        """Render the the clips into video.

        Args:
            custom_callback (Callable[[str, str], None]): A callable function
                for rendering process.

        Notes:
            `custom_callback` takes 2 integer parameters,
            `current_frame` and `total_frame`

        """
        # add clips
        # Notes:
        #    Clips must be added as layered on top of each other when
        #    bottom_clip + bottom_clip + bottom_clip + top_level_clip
        final_clip = CompositeVideoClip(
            clips=[self._video_file_clip] + self._image_clips + self._text_clips
        )
        audio_clip = CompositeAudioClip(clips=self._audio_clips)
        video_duration = audio_clip.duration + 1

        # set audio
        final_clip = final_clip.with_audio(audio_clip)
        final_clip = final_clip.with_duration(video_duration)

        # make sure videos folder exists
        if not isdir("videos"):
            mkdir("videos")

        # render
        filename = self.get_video_filepath()
        final_clip.write_videofile(
            filename,
            fps=30,
            audio_codec="aac",
            preset="fast",
            logger=custom_callback,
        )

    def close(self) -> None:
        """Free self from memory."""
        if self._video_file_clip:
            self._video_file_clip.close()

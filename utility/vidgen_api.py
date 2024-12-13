"""All API for generating the video."""

from PIL import ImageFont, Image
from moviepy import VideoFileClip

from exceptions.vid_gen_exceptions import NoVideoFileCLip


class VidGen:
    """The object to reuse and edit the video before rendering.

    Attributes:
        empty-yet

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
        self._video_height: int = 1920
        self._video_width: int = 1080

        # text positioning
        self._center_position_x = self._video_width // 2
        self._center_position_y = self._video_height // 2

        # text manipulation
        self._font_size: int = 80
        self._font: str = self.load_font()
        self._font_object = ImageFont.truetype(font=self._font, size=self._font_size)

    def load_video(self, filepath: str):
        """Lazily Load the video into moviepy.

        Args:
            filepath (str): The filepath of the video.

        """
        self._video_file_clip = VideoFileClip(filepath)

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

    def close(self) -> None:
        """Free self from memory."""
        if self._video_file_clip:
            self._video_file_clip.close()

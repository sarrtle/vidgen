"""All upload functions are handled here.

Videos will be uploaded as a Reel/Shorts

Notes:
    About their documentation

    Uploading to facebook pages have their own
    documentation here:
    https://developers.facebook.com/docs/video-api/guides/reels-publishing

Notes:
    About their limitations

    Facebook:
        aspect ratio: 9:16
        Resolution: 1080x1920
        fps: 24 to fps
        duration: 3 to 60 seconds

"""

# Upload to facebook
from typing import Callable
from customtkinter import CTkLabel
from models.config_data import ConfigData

import requests

from os.path import getsize


def upload_to_facebook(
    video_path: str,
    config_data: ConfigData,
    label_state: CTkLabel,
    done_callback: Callable[[bool, CTkLabel, str], None],
):
    """Upload to facebook.

    Args:
        video_path (str): The path of the video to upload.
        config_data (ConfigData): The configuration data.
        label_state (CTkLabel): Update the state of the label from ui.
        done_callback (Callable[[bool, CTkLabel, str], None]): Callback when upload is done.

    Raises:
        TODO:ErrorException

    """
    # unpack important variables
    facebook_token = config_data.api_settings.facebook_token
    facebook_page_id = config_data.api_settings.facebook_page

    # initialize an upload session
    # This step request a video id from facebook to
    # start the upload process with the video id
    url = f"https://graph.facebook.com/v22.0/{facebook_page_id}/video_reels"
    data = {"upload_phase": "START", "access_token": facebook_token}
    response = requests.post(url, json=data)

    if response.status_code != 200:
        done_callback(False, label_state, f"Status is {response.status_code}")
        return

    response_data = response.json()

    if "video_id" not in response_data or "upload_url" not in response_data:
        done_callback(False, label_state, "Video id not found")
        return

    # unpack response
    video_id = response_data.get("video_id")
    upload_url = response_data.get("upload_url")

    # Start upload
    file_size = getsize(video_path)
    binary_data = open(video_path, "rb").read()
    headers = {
        "Authorization": f"OAuth {facebook_token}",
        "offset": "0",
        "file_size": str(file_size),
    }

    response = requests.post(url=upload_url, headers=headers, data=binary_data)

    if response.status_code != 200:
        done_callback(
            False, label_state, f"Failed to start session: {response.status_code}"
        )
        return

    response_data = response.json()

    if "success" not in response_data:
        done_callback(False, label_state, "Upload not success")
        return

    # TODO: Yield the upload status or progress
    #           update progress from label ui

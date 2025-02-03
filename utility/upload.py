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
from time import sleep
from typing import Callable
from customtkinter import CTkLabel
from models.config_data import ConfigData

import requests

from os.path import getsize

from models.upload_model import UploadData


def upload_to_facebook(
    video_path: str,
    config_data: ConfigData,
    upload_data: UploadData,
    label_state: CTkLabel,
    done_callback: Callable[[bool, CTkLabel, str, str], None],
):
    """Upload to facebook.

    Args:
        video_path (str): The path of the video to upload.
        config_data (ConfigData): The configuration data.
        upload_data (UploadData): The upload data.
        label_state (CTkLabel): Update the state of the label from ui.
        done_callback (Callable[[bool, CTkLabel, str], None]): Callback when upload is done.

    Raises:
        TODO:ErrorException

    """
    # Initialize label state
    label_state.configure(text="Uploading...", text_color="#FFC107")

    # unpack important variables
    facebook_token = config_data.api_settings.facebook_token
    facebook_page_id = config_data.api_settings.facebook_page

    # initialize an upload session
    # This step request a video id from facebook to
    # start the upload process with the video id
    url = f"https://graph.facebook.com/v22.0/{facebook_page_id}/video_reels"
    data = {"upload_phase": "START", "access_token": facebook_token}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        done_callback(
            False,
            label_state,
            f"Failed to start session: {response.status_code}",
            video_path,
        )
        return

    response_data = response.json()

    if "video_id" not in response_data or "upload_url" not in response_data:
        done_callback(False, label_state, "Video id not found", video_path)
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
            False,
            label_state,
            f"Failed to start upload: {response.status_code}",
            video_path,
        )
        return

    response_data = response.json()

    if "success" not in response_data:
        done_callback(False, label_state, "Upload not success", video_path)
        return

    # progress status
    while True:
        url = f"https://graph.facebook.com/v22.0/{video_id}"
        params = {"access_token": facebook_token, "fields": "status"}

        response = requests.get(url, params=params)

        if response.status_code != 200:
            done_callback(
                False,
                label_state,
                f"Failed to upload: {response.status_code}",
                video_path,
            )
            return

        status_data = response.json().get("status")

        # This code seemed to be skipped because the upload phase status does not
        #   show any of the things in documentation and just proceed to "complete" it
        if status_data["uploading_phase"]["status"] in ["not_started", "in_progress"]:
            # calculate percentage and update label state
            bytes_transferred = status_data["uploading_phase"]["bytes_transferred"]
            total_size = status_data["uploading_phase"]["source_file_size"]

            # avoid division by zero
            if bytes_transferred == 0 or total_size == 0:
                continue

            percentage = (bytes_transferred / total_size) * 100
            label_state.configure(text=f"Uploading: {percentage:.2f}%")
            continue

        elif status_data["uploading_phase"]["status"] == "complete":
            done_callback(True, label_state, "Upload completed", video_path)

            # start publishing
            url = f"https://graph.facebook.com/v22.0/{facebook_page_id}/video_reels"
            parameters = {
                "access_token": facebook_token,
                "video_id": video_id,
                "upload_phase": "finish",
                "video_state": "PUBLISHED",
                "publish": "true",
                "description": upload_data.description + "\n" + upload_data.hashtags,
            }
            response = requests.post(url, params=parameters)

            if response.status_code != 200:
                done_callback(
                    False,
                    label_state,
                    f"Failed to publish: {response.status_code}",
                    video_path,
                )
                return

            return

        sleep(1)

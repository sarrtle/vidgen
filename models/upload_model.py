"""Upload model for all social media platforms."""

from dataclasses import dataclass


@dataclass
class UploadData:
    """Upload data model."""

    title: str
    description: str
    hashtags: str

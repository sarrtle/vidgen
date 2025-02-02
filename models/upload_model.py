"""Upload model for all social media platforms."""

from dataclasses import dataclass


@dataclass
class UploadData:
    """Upload data model."""

    description: str
    hashtags: str

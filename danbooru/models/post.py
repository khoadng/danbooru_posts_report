from dataclasses import dataclass

from datetime import datetime

@dataclass
class Post:
    id: int
    fav_count: int
    uploader_id: int
    approver_id: int
    rating: str
    source: str
    score: int
    createdAt: datetime
    is_pending: bool
    is_deleted: bool
    tags: list[str]
    artist_tags: list[str]
    copyright_tags: list[str]
    character_tags: list[str]
    general_tags: list[str]
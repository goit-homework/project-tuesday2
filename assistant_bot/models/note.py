from __future__ import annotations

from datetime import datetime
from .fields import Field


class Tag:
    def __init__(self, value: str):
        value = value.strip().lower()
        if not value:
            raise ValueError("Tag cannot be empty.")
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        if isinstance(other, Tag):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)


class Note:
    def __init__(self, title: str, content: str):
        title = title.strip()
        content = content.strip()

        if not title:
            raise ValueError("Note title cannot be empty.")
        if not content:
            raise ValueError("Note content cannot be empty.")

        self.id = None
        self.title = title
        self.content = content
        self.tags: set[Tag] = set()

    def add_tag(self, tag: str) -> None:
        self.tags.add(Tag(tag))

    def remove_tag(self, tag: str) -> None:
        tag_obj = Tag(tag)
        if tag_obj not in self.tags:
            raise ValueError("Tag not found.")
        self.tags.remove(tag_obj)

    def edit(self, new_title: str | None = None, new_content: str | None = None) -> None:
        if new_title is not None:
            new_title = new_title.strip()
            if not new_title:
                raise ValueError("Note title cannot be empty.")
            self.title = new_title

        if new_content is not None:
            new_content = new_content.strip()
            if not new_content:
                raise ValueError("Note content cannot be empty.")
            self.content = new_content

    def matches_query(self, query: str) -> bool:
        query = query.strip().lower()
        return query in self.title.lower() or query in self.content.lower()

    def has_tag(self, tag: str) -> bool:
        normalized = tag.strip().lower()
        return any(t.value == normalized for t in self.tags)

    def __str__(self) -> str:
        tags = ", ".join(sorted(str(tag) for tag in self.tags)) if self.tags else "No tags"
        return (
            f"[{self.id}] {self.title}\n"
            f"Content: {self.content}\n"
            f"Tags: {tags}"
        )

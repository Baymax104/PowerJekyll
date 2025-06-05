# -*- coding: UTF-8 -*-
import subprocess
from pathlib import Path

from core.models import Formatter, Item, Result
from core.repository import BlogRepository
from settings import Mode


class Blog:

    def __init__(self, root: Path, mode: Mode):
        self.root = root
        self.mode = mode
        self.repo = BlogRepository(root, mode)

    def synchronize(self) -> Result[None]:
        try:
            self.repo.update_index()
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

    def create(self, item: Item, formatter: Formatter) -> Result[None]:
        try:
            # name must be unique globally
            items = self.repo.posts + self.repo.drafts
            exist_item = next((i for i in items if i.name == item.name), None)
            if exist_item:
                raise ValueError(f"Item {item.name} already exists")
            self.repo.add(item, formatter)
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

    def remove(self, name: str) -> Result[None]:
        try:
            items = self.repo.posts + self.repo.drafts
            item = next((i for i in items if i.name == name), None)
            if item is None:
                raise ValueError(f"Item {name} not found")
            self.repo.remove(item)
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

    def open(self, name: str, editor: str | None = None) -> Result[None]:
        try:
            items = self.repo.posts + self.repo.drafts
            item = next((i for i in items if i.name == name), None)
            if item is None:
                raise ValueError(f"Item {name} not found")
            command = ["cmd.exe", "/c", "start", editor if editor else "", item.md_path]
            subprocess.run(command)
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

    def rename(self, name: str, new_name: str) -> Result[None]:
        try:
            items = self.repo.posts + self.repo.drafts
            item = next((i for i in items if i.name == name), None)
            if item is None:
                raise ValueError(f"Item {name} not found")
            self.repo.rename(item, new_name)
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

    def publish(self, name: str) -> Result[None]:
        try:
            items = self.repo.drafts
            item = next((i for i in items if i.name == name), None)
            if item is None:
                raise ValueError(f"Item {name} not found")
            self.repo.publish(item)
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

    def unpublish(self, name: str) -> Result[None]:
        try:
            items = self.repo.posts
            item = next((i for i in items if i.name == name), None)
            if item is None:
                raise ValueError(f"Item {name} not found")
            self.repo.unpublish(item)
            return Result.ok()
        except Exception as e:
            return Result.fail(e)

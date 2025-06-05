# -*- coding: UTF-8 -*-
from pathlib import Path

from core.models import BlogItems, Formatter, Item
from core.repository.directory_dao import DirectoryDao
from core.repository.file_dao import FileDao
from core.repository.items import get_from_index, get_from_root
from settings import Mode


class BlogRepository:

    def __init__(self, root: Path, mode: Mode):
        self.root = root
        self.mode = mode
        self.__items: BlogItems | None = None
        if mode == Mode.File:
            self.dao = FileDao(root=root)
        elif mode == Mode.Directory:
            self.dao = DirectoryDao(root=root)
        else:
            raise NotImplementedError

    def update_index(self):
        items = get_from_root(self.root, self.mode)
        index_file = Path.home() / ".jekyll-cli" / f"index-{self.mode}.json"
        content = items.model_dump_json(indent=2)
        index_file.write_text(content, encoding="utf-8")

    def __get_items(self) -> BlogItems | None:
        try:
            if self.__items is None:
                index_file = Path().home() / ".jekyll-cli" / f"index-{self.mode}.json"
                if not index_file.is_file():
                    self.update_index()
                self.__items = get_from_index(self.mode)
            return self.__items
        except Exception:
            return None

    @property
    def posts(self) -> list[Item]:
        return list(self.__get_items().posts)

    @property
    def drafts(self) -> list[Item]:
        return list(self.__get_items().drafts)

    def add(self, item: Item, formatter: Formatter):
        self.dao.add(item, formatter)
        self.update_index()

    def remove(self, item: Item):
        self.dao.remove(item)
        self.update_index()

    def rename(self, item: Item, new_name: str):
        self.dao.rename(item, new_name)
        self.update_index()

    def publish(self, item: Item):
        self.dao.publish(item)
        self.update_index()

    def unpublish(self, item: Item):
        self.dao.unpublish(item)
        self.update_index()

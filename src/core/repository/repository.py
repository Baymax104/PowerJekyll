# -*- coding: UTF-8 -*-
from pathlib import Path

from core.models import BlogItems, Formatter, Item
from core.repository.directory_dao import DirectoryDao
from core.repository.file_dao import FileDao
from core.utils import is_dir_item, is_file_item, load_item
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
        items = self.__get_from_root()
        index_file = Path.home() / ".jekyll-cli" / f"index-{self.mode}.json"
        content = items.model_dump_json(indent=4)
        index_file.write_text(content, encoding="utf-8")

    def __get_from_root(self) -> BlogItems:
        def get_from_sub_dir(sub_dir: str) -> list[Item]:
            parent_dir = self.root / sub_dir
            filter_item = is_file_item if self.mode == Mode.File else is_dir_item
            item_paths = [f for f in parent_dir.iterdir() if filter_item(f)]
            items = [load_item(f, self.root) for f in item_paths]
            return items

        posts = get_from_sub_dir("_posts")
        drafts = get_from_sub_dir("_drafts")
        return BlogItems(posts=posts, drafts=drafts)

    def __get_from_index(self) -> BlogItems:
        index_abs_path = Path().home() / ".jekyll-cli" / f"index-{self.mode}.json"
        content = index_abs_path.read_text(encoding="utf-8")
        return BlogItems.model_validate_json(content)

    def __get_items(self) -> BlogItems | None:
        try:
            if self.__items is None:
                index_file = Path().home() / ".jekyll-cli" / f"index-{self.mode}.json"
                if not index_file.is_file():
                    self.update_index()
                self.__items = self.__get_from_index()
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

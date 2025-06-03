# -*- coding: UTF-8 -*-
from pathlib import Path

from core.models import BlogItems, Formatter, Item
from core.service import BlogService
from core.utils import is_dir_item, is_file_item, load_item
from settings import Mode


class Blog:

    def __init__(self, root: Path, mode: Mode):
        self.root = root
        self.mode = mode
        self.service = BlogService(root, mode)


    def synchronize(self):
        posts = self.__get_items("_posts")
        drafts = self.__get_items("_drafts")
        blog_items = BlogItems(posts=posts, drafts=drafts)
        index_file = Path.home() / ".jekyll-cli" / "index.json"
        content = blog_items.model_dump_json(indent=4)
        index_file.write_text(content, encoding="utf-8")


    def __get_items(self, sub_dir: str) -> list[Item]:
        parent_dir = self.root / sub_dir
        filter_item = is_file_item if self.mode == Mode.File else is_dir_item
        item_paths = [f for f in parent_dir.iterdir() if filter_item(f)]
        items = [load_item(f, self.root) for f in item_paths]
        return items


    def create(self, item: Item, formatter: Formatter):
        self.service.create(item, formatter)


    def remove(self, item: Item):
        self.service.remove(item)


    def open(self, item: Item, editor: str | None = None):
        self.service.open(item, editor)


    def rename(self, item: Item, new_name: str):
        self.service.rename(item, new_name)


    def publish(self, item: Item):
        self.service.publish(item)


    def unpublish(self, item: Item):
        self.service.unpublish(item)


if __name__ == "__main__":
    root = Path("D:/baymax104.github.io")
    blog = Blog(root, Mode.Directory)
    blog.synchronize()

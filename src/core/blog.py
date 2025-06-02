# -*- coding: UTF-8 -*-
import json
from pathlib import Path

from settings import Mode
from .models import Item
from .service import BlogService
from .utils import is_dir_item, is_file_item, load_item


class Blog:

    def __init__(self, root: Path, mode: Mode):
        self.root = root
        self.mode = mode
        self.service = BlogService(root, mode)


    def synchronize(self):
        posts = self.__get_items("_posts")
        posts = [item.model_dump() for item in posts]
        drafts = self.__get_items("_drafts")
        drafts = [item.model_dump() for item in drafts]

        data = {
            "posts": posts,
            "drafts": drafts,
        }

        index_file = Path.home() / ".jekyll-cli" / "index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    def __get_items(self, sub_dir: str) -> list[Item]:
        parent_dir = self.root / sub_dir
        if self.mode == Mode.File:
            item_paths = [f for f in parent_dir.iterdir() if is_file_item(f)]
        else:
            item_paths = [f for f in parent_dir.iterdir() if is_dir_item(f)]

        items = [load_item(f) for f in item_paths]
        return items


if __name__ == "__main__":
    root = Path("D:/baymax104.github.io")
    blog = Blog(root, Mode.Directory)
    blog.synchronize()

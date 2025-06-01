# -*- coding: UTF-8 -*-
import re
import shutil
import subprocess
import time

from ruamel.yaml import YAML

from blog.models import Item, ItemType
from blog.service.base import BaseService
from blog.utils import assert_item_exists


class DirectoryService(BaseService):

    def create(self, item: Item):
        sub_dir = "_posts" if item.type == ItemType.Post else "_drafts"
        item_path = self.root / sub_dir / item.name
        assets_path = item_path / "assets"
        md_filename = f"{item.name}.md"
        if item.type == ItemType.Post:
            md_filename = f"{time.strftime('%Y-%m-%d')}-{md_filename}"
        md_path = item_path / md_filename

        if item.type == ItemType.Post:
            item.formatter.date = time.strftime("%Y-%m-%d %H:%M")
        item.path = item_path
        item.md_path = md_path

        item_path.mkdir(exist_ok=True)
        assets_path.mkdir(exist_ok=True)
        with open(item.md_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            YAML().dump(item.formatter.model_dump(), f)
            f.write("---\n")


    def open(self, item: Item, editor: str | None = None):
        assert_item_exists(item)
        command = ["cmd.exe", "/c", "start", editor if editor else "", item.md_path]
        subprocess.run(command)


    def remove(self, item: Item):
        assert_item_exists(item)
        shutil.rmtree(item.path)


    def rename(self, item: Item, new_name: str):
        assert_item_exists(item)

        pattern = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)")
        if item.type == ItemType.Post and (match := pattern.match(item.md_path.stem)):
            new_stem = f"{match.group(1)}-{new_name}"
        else:
            new_stem = new_name

        md_path = item.md_path.with_stem(new_stem)
        item_path = item.path.with_name(new_name)

        if item_path.exists():
            raise ValueError("Item path already exists.")

        item.md_path.rename(md_path)
        item.path.rename(item_path)


    def publish(self, item: Item):
        assert_item_exists(item)
        if item.type == ItemType.Post:
            raise ValueError("Cannot publish Post")

        dest_parent_dir = self.root / "_posts"
        dest_path = dest_parent_dir / item.path.relative_to(item.parent)
        dest_md_path = dest_parent_dir / item.md_path.relative_to(item.parent)
        shutil.move(item.path, dest_path)

        item.formatter.date = time.strftime("%Y-%m-%d %H:%M")

        with open(dest_md_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            YAML().dump(item.formatter.model_dump(), f)
            f.write("---\n")


    def unpublish(self, item: Item):
        assert_item_exists(item)
        if item.type == ItemType.Draft:
            raise ValueError("Cannot unpublish Draft")

        dest_parent_dir = self.root / "_drafts"
        dest_path = dest_parent_dir / item.path.relative_to(item.parent)
        dest_md_path = dest_parent_dir / item.md_path.relative_to(item.parent)
        shutil.move(item.path, dest_path)

        item.formatter.date = None

        with open(dest_md_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            YAML().dump(item.formatter.model_dump(), f)
            f.write("---\n")

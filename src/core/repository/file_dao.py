# -*- coding: UTF-8 -*-
import re
import shutil
import subprocess
import time

from ruamel.yaml import YAML

from core.models import Formatter, Item, ItemType
from core.repository.common import BaseDao
from core.utils import assert_item_exists


class FileDao(BaseDao):

    def add(self, item: Item, formatter: Formatter):
        md_filename = f"{item.name}.md"
        if item.type == ItemType.Post:
            md_filename = f"{time.strftime('%Y-%m-%d')}-{md_filename}"
        sub_dir = "_posts" if item.type == ItemType.Post else "_drafts"
        item_abs_path = self.root / sub_dir / md_filename

        if item.type == ItemType.Post:
            formatter.date = time.strftime("%Y-%m-%d %H:%M")
        item.path = item_abs_path.relative_to(self.root)
        item.md_path = item_abs_path.relative_to(self.root)

        yaml = YAML(typ="string")
        content = f"---\n{yaml.dump_to_string(formatter.model_dump())}\n---\n"
        item_abs_path.write_text(content, encoding="utf-8")


    def open(self, item: Item, editor: str | None = None):
        assert_item_exists(item)
        command = ["cmd.exe", "/c", "start", editor if editor else "", item.md_path]
        subprocess.run(command)


    def remove(self, item: Item):
        assert_item_exists(item)
        item.path.unlink()


    def rename(self, item: Item, new_name: str):
        assert_item_exists(item)

        pattern = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)")
        if item.type == ItemType.Post and (match := pattern.match(item.md_path.stem)):
            new_stem = f"{match.group(1)}-{new_name}"
        else:
            new_stem = new_name

        md_path = self.root / item.md_path.with_stem(new_stem)
        if md_path.exists():
            raise ValueError("Item path already exists.")
        (self.root / item.md_path).rename(md_path)


    def publish(self, item: Item):
        assert_item_exists(item)
        if item.type == ItemType.Post:
            raise ValueError("Cannot publish Post")

        dest_parent_abs_path = self.root / "_posts"
        dest_item_abs_path = dest_parent_abs_path / item.path.relative_to(item.parent)
        shutil.move(self.root / item.path, dest_item_abs_path)


    def unpublish(self, item: Item):
        assert_item_exists(item)
        if item.type == ItemType.Draft:
            raise ValueError("Cannot unpublish Draft")

        dest_parent_abs_path = self.root / "_drafts"
        dest_item_abs_path = dest_parent_abs_path / item.path.relative_to(item.parent)
        shutil.move(self.root / item.path, dest_item_abs_path)

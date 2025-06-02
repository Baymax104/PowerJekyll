# -*- coding: UTF-8 -*-
from datetime import date
from pathlib import Path

from ruamel.yaml import YAML

from core.models import Formatter, Item, ItemType


def __load_formatter(formatter: str) -> Formatter:
    formatter = YAML().load(formatter) if formatter else {}
    if "date" in formatter and isinstance(formatter["date"], date):
        formatter["date"] = formatter["date"].strftime("%Y-%m-%d %H:%M")
    if "tags" in formatter and isinstance(formatter["tags"], str):
        formatter["tags"] = formatter["tags"].split(" ")
    if "categories" in formatter and isinstance(formatter["categories"], str):
        formatter["categories"] = formatter["categories"].split(" ")
    formatter = Formatter(**formatter)
    return formatter


def load_item(item_path: Path) -> Item:
    if item_path.is_file() and item_path.suffix == ".md":
        md_path = item_path
    elif item_path.is_dir():
        # 取第一个md
        md_path = next(item_path.glob("*.md"), None)
    else:
        md_path = None

    if md_path is None:
        raise ValueError("md_path is not found")

    if item_path.parent.name == "_drafts":
        item_type = ItemType.Draft
    elif item_path.parent.name == "_posts":
        item_type = ItemType.Post
    else:
        raise ValueError("Unexpected item type")

    content = md_path.read_text(encoding="utf-8")
    parts = content.split('---\n', maxsplit=2)
    formatter = __load_formatter(parts[1])
    article = parts[2]

    item = Item(
        name=item_path.stem,
        type=item_type,
        path=item_path,
        md_path=md_path,
        formatter=formatter,
        article=article
    )
    return item

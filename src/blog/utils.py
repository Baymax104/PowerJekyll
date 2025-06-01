# -*- coding: UTF-8 -*-
from pathlib import Path

from ruamel.yaml import YAML

from blog.models import Formatter, Item, ItemType


def load_item(item_path: Path) -> Item:
    if not item_path.exists():
        raise ValueError("item.path is not found")
    if item_path.is_file() and item_path.suffix == ".md":
        md_path = item_path
    elif item_path.is_dir():
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

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---\n', maxsplit=2)
    formatter = YAML().load(parts[1]) if parts[1] else {}
    formatter = Formatter(**formatter)
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


def assert_item_exists(item: Item):
    if item.path is None or not item.path.exists():
        raise ValueError('Item path is null.')
    if item.md_path is None or not item.md_path.exists():
        raise ValueError('File path is null.')

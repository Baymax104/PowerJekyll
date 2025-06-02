# -*- coding: UTF-8 -*-
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field


class ItemType(StrEnum):
    Post = "post"
    Draft = "draft"


class Formatter(BaseModel):
    model_config = ConfigDict(extra="allow")

    layout: Annotated[str, Field(frozen=True)] = "post"
    title: str = ""
    categories: list[str] = []
    tags: list[str] = []
    date: str | None = None


class Item(BaseModel):
    name: str
    type: ItemType
    path: Path | None = None
    md_path: Path | None = None
    formatter: Formatter = Formatter()
    article: str = ""


    @property
    def parent(self) -> Path | None:
        return self.path.parent if self.path else None


    @property
    def info(self) -> dict[str, Any]:
        infos = {
            "name": self.name,
            "type": self.type.name,
            "path": str(self.path),
            "markdown path": str(self.md_path),
        }
        infos = dict(infos, **self.formatter.model_dump())
        return infos

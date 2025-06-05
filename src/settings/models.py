# -*- coding: UTF-8 -*-
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel


class Mode(StrEnum):
    File = "file"
    Directory = "directory"


class GenerateSettings(BaseModel):
    draft: bool = False
    port: int = 4000


class AppSettings(BaseModel):
    root: Path | None = None
    mode: Mode
    generate: GenerateSettings = GenerateSettings()
    editor: str | None = None

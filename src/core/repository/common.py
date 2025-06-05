# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel

from core.models import Formatter, Item


class DaoOperation(ABC):

    @abstractmethod
    def add(self, item: Item, formatter: Formatter):
        ...


    @abstractmethod
    def remove(self, item: Item):
        ...


    @abstractmethod
    def rename(self, item: Item, new_name: str):
        ...


    @abstractmethod
    def publish(self, item: Item):
        ...


    @abstractmethod
    def unpublish(self, item: Item):
        ...


class BaseDao(DaoOperation, BaseModel, ABC):
    root: Path

# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel

from core.models import Item


class ServiceOperation(ABC):

    @abstractmethod
    def create(self, item: Item):
        ...


    @abstractmethod
    def open(self, item: Item, editor: str | None = None):
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


class BaseService(ServiceOperation, BaseModel, ABC):
    root: Path

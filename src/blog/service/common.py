# -*- coding: UTF-8 -*-
from pathlib import Path

from blog.models import Item
from blog.service.base import ServiceOperation
from blog.service.directory_service import DirectoryService
from blog.service.file_service import FileService
from settings import Mode


class BlogService(ServiceOperation):

    def __init__(self, root: Path, mode: Mode):
        if mode == Mode.File:
            self.delegate = FileService(root=root)
        elif mode == Mode.Directory:
            self.delegate = DirectoryService(root=root)
        else:
            raise NotImplementedError


    def create(self, item: Item):
        self.delegate.create(item)


    def open(self, item: Item, editor: str | None = None):
        self.delegate.open(item, editor)


    def remove(self, item: Item):
        self.delegate.remove(item)


    def rename(self, item: Item, new_name: str):
        self.delegate.rename(item, new_name)


    def publish(self, item: Item):
        self.delegate.publish(item)


    def unpublish(self, item: Item):
        self.delegate.unpublish(item)

"""
A simple util for dispatcher for storage your data. e.g: database connection, messages count.
"""
import typing
from abc import ABC
from abc import abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def place(self, key: typing.AnyStr, value: typing.Any) -> None:
        """
        Place value to storage.
        :param key:
        :param value:
        :return:
        """

    @abstractmethod
    def get(
        self, key: typing.AnyStr, default: typing.Any = None
    ) -> typing.Optional[typing.Any]:
        """
        Get value by key from storage or get default value.
        :param key:
        :param default:
        :return:
        """

    @abstractmethod
    def delete(self, key: typing.AnyStr) -> None:
        """
        Delete key/value from storage by key
        :param key:
        :return:
        """

    @abstractmethod
    def update(self, key: typing.AnyStr, value: typing.Any):
        """
        Update value in storage by key.
        :param key:
        :param value:
        :return:
        """


class Storage(AbstractStorage):
    def place(self, key: typing.AnyStr, value: typing.Any) -> None:
        if hasattr(self, key):
            raise RuntimeError("Storage already have this key.")
        setattr(self, key, value)

    def get(
        self, key: typing.AnyStr, default: typing.Any = None
    ) -> typing.Optional[typing.Any]:
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return default

    def delete(self, key: typing.AnyStr) -> None:
        if hasattr(self, key):
            delattr(self, key)
        else:
            raise RuntimeError("Undefined key.")

    def update(self, key: typing.AnyStr, value: typing.Any):
        if not hasattr(self, key):
            raise RuntimeError("Storage don`t have this key.")
        setattr(self, key, value)

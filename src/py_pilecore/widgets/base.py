import json
import os
from abc import ABC, abstractmethod, abstractproperty

from IPython.display import display
from ipywidgets import Widget


class BaseCoreWidget(ABC):
    name: str

    def __init__(
        self, cache_name: str = "default", cache_dir: str = ".pylecore/cache"
    ) -> None:
        self._cache_dir = cache_dir
        self.cache_name = cache_name

        self.ipywidget = self._init_ipywidget()

        self._load_or_save_cache()
        self._cache_values()

        self.display()

    @property
    def cache_name_dir(self) -> str:
        return os.path.join(self._cache_dir, self.cache_name)

    @property
    def widget_cache_path(self) -> str:
        return os.path.join(self.cache_name_dir, self.name + ".json")

    @abstractproperty
    def values(self) -> dict:
        ...

    def _load_cache(self) -> None:
        ...

    def _load_or_save_cache(self) -> None:
        if os.path.exists(self.widget_cache_path):
            self._load_cache()
        else:
            self._cache_values()

    def _cache_values(self) -> None:
        if not os.path.exists(self.cache_name_dir):
            os.makedirs(self.cache_name_dir)

        with open(self.widget_cache_path, "w+") as cache_file:
            json.dump(self.values, cache_file)

    @abstractmethod
    def _init_ipywidget(self) -> Widget:
        ...

    def display(self) -> None:
        display(self.ipywidget)

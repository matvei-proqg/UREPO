import importlib
import pkgutil
from typing import Dict, Type
from pathlib import Path

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugins: Dict[str, Type] = {}
        self.plugin_dir = Path(plugin_dir)

    def load_plugins(self):
        """Загрузка всех плагинов из директории"""
        for finder, name, _ in pkgutil.iter_modules([str(self.plugin_dir)]):
            module = importlib.import_module(f"plugins.{name}")
            if hasattr(module, "Plugin"):
                self.plugins[name] = module.Plugin

    def execute_hook(self, hook_name: str, *args, **kwargs):
        """Выполнение хука во всех плагинах"""
        for plugin in self.plugins.values():
            if hasattr(plugin, hook_name):
                getattr(plugin, hook_name)(*args, **kwargs)

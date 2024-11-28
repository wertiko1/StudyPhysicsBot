import sys
from os import walk
from pathlib import Path
from types import ModuleType
from typing import Optional

from aiogram import Router, Dispatcher
from loguru import logger


class RoutersLoader:
    def __init__(self, routers_path: str, dp: Dispatcher) -> None:
        self._routers_path: str = routers_path
        self._routers_import: str = routers_path.replace('/', '.')
        self._dispatcher: Dispatcher = dp

    def load(self) -> None:
        try:
            router_files: list[Path] = []
            for root, _, files in walk(self._routers_path):
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        router_files.append(Path(root) / file)

            logger.info(f"Found {len(router_files)} routers to load.")

            for file in router_files:
                self._load_router(file)

            logger.info("All routers have been successfully loaded.")
        except Exception as error:
            logger.exception(f"Error while loading routers from directory '{self._routers_path}': {error}")

    def _load_router(self, file_path: Path) -> None:
        relative_path = file_path.relative_to(self._routers_path).with_suffix("")
        router_name: str = str(relative_path).replace('/', '.')
        try:
            logger.info(f"Attempting to load router: {router_name}")
            router_module: Optional[ModuleType] = self._import_router(f"{self._routers_import}.{router_name}")

            if not hasattr(router_module, 'router'):
                logger.warning(f"Module '{router_name}' does not contain a 'router' object. Skipping.")
                return

            router = getattr(router_module, 'router')
            if not isinstance(router, Router):
                raise ValueError(
                    f"Expected 'router' in module '{router_name}' to be an instance of Router, "
                    f"but got {type(router).__name__}."
                )

            self._dispatcher.include_router(router)
            logger.info(f"Router '{router_name}' successfully loaded and connected.")
        except Exception as error:
            logger.error(f"Error while loading router '{router_name}': {error}", exc_info=True)

    def _import_router(self, module_name: str) -> ModuleType:
        try:
            logger.debug(f"Importing module: {module_name}")
            __import__(module_name)
            module: Optional[ModuleType] = sys.modules.get(module_name)
            if module:
                logger.debug(f"Module '{module_name}' successfully imported.")
                return module
            else:
                raise ImportError(f"Module '{module_name}' not found in sys.modules.")
        except ImportError as error:
            logger.error(f"Error importing module '{module_name}': {error}")
            raise

import importlib
import pkgutil

# from pathlib import Path
from typing import List
from fastapi import APIRouter, FastAPI
from loguru import logger

from ..core.config import Settings


class Routers:
    def __init__(self, app: FastAPI, settings: Settings):
        self.app = app
        self.settings = settings

    def _include_router(self, router):
        self.app.include_router(
            router, prefix=f"{self.settings.API_PREFIX}", tags=router.tags
        )

    def include_routers(self, routers):
        for router in routers:
            self._include_router(router)

    def discover_and_include_routers(self):
        """Discover and include all routers from modules/*/router.py"""
        routers = self._discover_routers()
        if routers:
            logger.info(f"Discovered {len(routers)} routers:")
            for router in routers:
                module_name = getattr(router, "_module_name", "Unknown")
                logger.info(f"  - {module_name}")
            self.include_routers(routers)
        else:
            logger.warning("No routers found in modules")

    def _discover_routers(self) -> List[APIRouter]:
        """Discover all routers from modules/*/router.py"""
        routers = []
        modules_package_name = "apiapp.modules"

        try:
            # Import the modules package
            modules_package = importlib.import_module(modules_package_name)

            # Get all modules in the modules package
            for finder, module_name, ispkg in pkgutil.iter_modules(
                modules_package.__path__, modules_package.__name__ + "."
            ):
                if ispkg:  # Only process sub-packages (feature modules)
                    try:
                        # Try to import router from the module
                        router_module_name = f"{module_name}.router"
                        router_module = importlib.import_module(router_module_name)

                        # Get the router object
                        if hasattr(router_module, "router"):
                            router = getattr(router_module, "router")
                            if isinstance(router, APIRouter):
                                # Add module name for logging
                                router._module_name = module_name.split(".")[-1]
                                routers.append(router)
                                logger.debug(f"Found router in {router_module_name}")
                            else:
                                logger.warning(
                                    f"'router' in {router_module_name} is not an APIRouter instance"
                                )
                        else:
                            logger.warning(
                                f"No 'router' attribute found in {router_module_name}"
                            )

                    except ImportError as e:
                        logger.debug(f"No router.py found in {module_name}: {e}")
                        continue
                    except Exception as e:
                        logger.warning(
                            f"Error importing router from {module_name}: {e}"
                        )
                        continue

        except Exception as e:
            logger.error(
                f"Could not import modules package {modules_package_name}: {e}"
            )
            return []

        return routers


def init_routers(app: FastAPI, settings: Settings) -> Routers:
    """Initialize all routers from modules"""
    router_manager = Routers(app, settings)
    router_manager.discover_and_include_routers()
    return router_manager

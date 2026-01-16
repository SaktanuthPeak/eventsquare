import importlib
import pathlib

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from loguru import logger

from ..utils.http_error import http_error_handler
from ..utils.validation_error import http422_error_handler


async def init_router(app: FastAPI, settings):
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

    current_directory = pathlib.Path(__file__).parent
    routers = await get_subrouters(current_directory)

    logger.info(f"routers {[(lambda r: r.prefix)(r) for r in routers]}")
    for router in routers:
        # logger.debug(f"{router.tags}")
        app.include_router(router, prefix=f"{settings.API_PREFIX}", tags=router.tags)


async def get_subrouters(directory):
    routers = []

    package = directory.parts[len(pathlib.Path.cwd().parts) :]
    parent_router = None

    try:
        pymod_file = f"{'.'.join(package)}"
        pymod = importlib.import_module(pymod_file)

        if "router" in dir(pymod):
            parent_router = pymod.router
            routers.append(parent_router)
    except Exception as e:
        logger.exception(e)
        return routers

    subrouters = []
    for module in directory.iterdir():
        if "__" == module.name[:2]:
            continue

        if module.match("*.py"):
            try:
                pymod_file = f"{'.'.join(package)}.{module.stem}"
                pymod = importlib.import_module(pymod_file)

                if "router" in dir(pymod):
                    subrouters.append(pymod.router)
            except Exception as e:
                logger.exception(e)

        elif module.is_dir():
            subrouters.extend(await get_subrouters(module))

    logger.info(f"router {[(lambda r: r.prefix)(r) for r in subrouters]}")
    for router in subrouters:
        # logger.debug(f"router {router.prefix}")
        if parent_router:
            parent_router.include_router(router)
        else:
            routers.append(router)

    return routers

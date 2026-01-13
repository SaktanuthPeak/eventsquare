from .server import ControllerServer


def create_server():
    from ..core.config import get_settings

    settings = get_settings()
    server = ControllerServer(settings)

    return server

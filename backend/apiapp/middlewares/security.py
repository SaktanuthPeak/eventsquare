from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette import status
from loguru import logger

from ..core.config import Settings


def init_security_middleware(app: FastAPI, settings: Settings) -> None:
    """Initialize security middleware for user agent filtering"""
    
    @app.middleware("http")
    async def filter_user_agents(request: Request, call_next):
        user_agent = request.headers.get("user-agent", "")
        logger.debug(f"user-agent ==> {user_agent}")
        
        for agent in settings.DISALLOW_AGENTS:
            if agent in user_agent.lower():
                logger.warning({"detail": "Client is not allow to uses."})
                return JSONResponse(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    content={"detail": "Client is not allow to uses."},
                )
        
        response: Response = await call_next(request)
        return response

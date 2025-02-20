import logging

import fastapi.openapi.utils as utils
from api import accounts, authentication, html_pages
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, StrictStr

server = FastAPI(
    title="Super Patient",
    description="All the private and public APIs for the Super Patient",
    version="0.1.0",
)

server.mount("/static", StaticFiles(directory="static"), name="static")

# Add all the API services here exposed to the public
server.include_router(authentication.router)
server.include_router(accounts.router)
server.include_router(html_pages.router)


@server.exception_handler(Exception)
async def server_error_exception_handler(request: Request, exc: Exception):
    """
    Handle all unknown exceptions

    :param request: The http request object
    :type request: Request
    :param exc: The exception object
    :type exc: Exception
    """
    message = f"Unkown Exception: {str(exc)} in request: {request.method} {request.url}"
    # Log the error to the uvicorn logger
    logger = logging.getLogger("uvicorn.error")
    logger.error(message)

import logging

import fastapi.openapi.utils as utils
from api import accounts, authentication
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, StrictStr

server = FastAPI(
    title="SAIL",
    description="All the private and public APIs for the Secure AI Labs",
    version="0.1.0",
)


# Add all the API services here exposed to the public
server.include_router(authentication.router)
server.include_router(accounts.router)


# Override the default validation error handler as it throws away a lot of information
# about the schema of the request body.
class ValidationError(BaseModel):
    error: StrictStr = Field(default="Invalid Schema")


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error = ValidationError(error="Invalid Schema")
    return JSONResponse(status_code=422, content=jsonable_encoder(error))


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


utils.validation_error_response_definition = ValidationError.schema()

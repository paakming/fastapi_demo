from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from app.models.response import ResponseCode, ResultResponse

from .service_exception import ServiceException


def global_excetption_handler(app: FastAPI):
    @app.exception_handler(ServiceException)
    async def service_exception_handler(request: Request, exc: ServiceException):
        logger.info(f'{request.method} {request.url} {exc.code} {exc.message}')
        return JSONResponse(
            status_code=ResponseCode.SUCCESS,
            content=ResultResponse.error(code=exc.code, message=exc.message).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.info(f'{request.method} {request.url} {exc.status_code} {exc.detail}')
        return JSONResponse(
            status_code=ResponseCode.SUCCESS,
            content=ResultResponse.error(code=exc.status_code, message=exc.detail).model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def padantic_validation_exception_handler(request: Request, exc: ValidationError):
        logger.info(f'{request.method} {request.url} {HTTPStatus.BAD_REQUEST} {exc.errors()}')
        return JSONResponse(
            status_code=ResponseCode.SUCCESS,
            content=ResultResponse.error(code=HTTPStatus.BAD_REQUEST, message='pydantic 验证异常').model_dump(),
        )

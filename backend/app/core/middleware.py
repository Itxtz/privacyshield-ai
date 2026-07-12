import time

from datetime import datetime

from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        process_time_ms = process_time * 1000 #Converting the time to milliseconds for readability

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        logger.info(
            "\n"
            + "=" * 60
            + f"\nTime           : {current_time}"
            + f"\nMethod         : {request.method}"
            + f"\nPath           : {request.url.path}"
            + f"\nStatus Code    : {response.status_code}"
            + f"\nExecution Time : {process_time_ms:.2f} ms"
            + "\n"
            + "=" * 60
        )

        return response
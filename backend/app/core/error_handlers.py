from fastapi import Request, HTTPException

from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError

from slowapi.errors import RateLimitExceeded

async def http_exception_handler(

    request: Request,

    exc: HTTPException

):
    
    return JSONResponse(

        status_code=exc.status_code,

        content={
            "success": False,

            "status_code": exc.status_code,

            "error": exc.detail
        }
    )

async def validation_exception_handler(

    request: Request,

    exc: RequestValidationError

):

    errors = []

    for error in exc.errors():

        errors.append(

            {

                "field": ".".join(
                    str(item)
                    for item in error["loc"]
                ),

                "message": error["msg"]

            }

        )

    return JSONResponse(

        status_code=422,

        content={

            "success": False,

            "status_code": 422,

            "error": "Validation failed",

            "details": errors

        }

    )

async def rate_limit_exception_handler(
    request,
    exc: RateLimitExceeded
):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "status_code": 429,
            "error": "Too many requests. Please try again later."
        }
    )
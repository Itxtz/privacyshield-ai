from fastapi import HTTPException


class NotFoundException(HTTPException):

    def __init__(self, detail: str = "Resource not found."):

        super().__init__(
            status_code=404,
            detail=detail
        )

class ForbiddenException(HTTPException):

    def __init__(self, detail: str = "Access denied."):

        super().__init__(
            status_code=403,
            detail=detail
        )

class BadRequestException(HTTPException):

    def __init__(self, detail: str = "Bad request."):

        super().__init__(
            status_code=400,
            detail=detail
        )

class ConflictException(HTTPException):

    def __init__(self, detail: str = "Conflict."):

        super().__init__(
            status_code=409,
            detail=detail
        )

class UnauthorizedException(HTTPException):

    def __init__(self, detail: str = "Unauthorized."):

        super().__init__(
            status_code=401,
            detail=detail
        )

class InactiveAccountException(HTTPException):

    def __init__(
        self,
        detail: str = (
            "Your account has been disabled. "
            "Please contact the administrator."
        )
    ):

        super().__init__(
            status_code=403,
            detail=detail
        )

class InvalidCredentialsException(HTTPException):

    def __init__(
        self,
        detail: str = "Invalid credentials"
    ):

        super().__init__(
            status_code=401,
            detail=detail
        )

class AdminPrivilegesRequiredException(HTTPException):

    def __init__(
        self,
        detail: str = "Admin privileges required."
    ):

        super().__init__(
            status_code=403,
            detail=detail
        )
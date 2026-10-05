class AppError(Exception):
    """Base exception for application-level errors."""

    code = "APPLICATION_ERROR"
    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    code = "NOT_FOUND"
    status_code = 404


class UnauthorizedError(AppError):
    """Raised when authentication is required or invalid."""

    code = "UNAUTHORIZED"
    status_code = 401


class ForbiddenError(AppError):
    """Raised when the authenticated user is not allowed to perform an action."""

    code = "FORBIDDEN"
    status_code = 403


class ValidationError(AppError):
    """Raised when application-level validation fails."""

    code = "VALIDATION_ERROR"
    status_code = 400
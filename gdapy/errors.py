class GDServerError(Exception):
    """Base exception for all GD API errors.

    Attributes:
        error_code (int): The specific error code returned by the servers
    """

    def __init__(self, error_code: int, message: str = ""):
        if not message:
            message = f"Got error code {error_code} from servers!"
        super().__init__(message)
        self.error_code = error_code

class NotLoggedInError(Exception):
    def __init__(self):
        super().__init__("Not logged in for endpoint that requires user credentials!")

class NotImplementedModEndpointError(NotImplementedError):
    pass

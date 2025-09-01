class ServiceException(Exception):
    def __init__(self, code: int = 500, message: str = 'error'):
        self.code = code
        self.message = message

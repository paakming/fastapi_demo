from pydantic import BaseModel

class ResponResult(BaseModel):
    code: int
    msg: str
    result: list | dict = []

    @staticmethod
    def success(code: int = 200, msg: str = "", result: list | dict = None) -> dict:
        result = result or []
        return {"code": code, "msg": msg, "result": result}
    
    @staticmethod
    def error(code: int = 500, msg: str = "", result: list = None) -> dict:
        result = result or []
        return {"code": code, "msg": msg, "result": result}
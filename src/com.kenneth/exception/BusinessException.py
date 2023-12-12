class BusinessException:
    code: str
    message: str

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def build(self):
        return {"code": self.code, "message": self.message}

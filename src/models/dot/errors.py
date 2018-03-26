class AdminError(Exception):
    def __init__(self, msg):
        self.msg = msg

class AdminNotExistError(AdminError):
    pass

class PasswordIncorrectError(AdminError):
    pass

class EmailNotValidError(AdminError):
    pass
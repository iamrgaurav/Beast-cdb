class APIErrors(Exception):
    def __init__(self,msg):
        self.msg = msg

class UserNotExist(APIErrors):
    pass

class PasswordIncorrect(APIErrors):
    pass
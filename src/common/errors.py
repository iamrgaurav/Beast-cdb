class Errors(Exception):
    def __init__(self, msg):
        self.msg = msg

class NameError(Errors):
    pass

class AadhaarError(Errors):
    pass

class PhoneError(Errors):
    pass
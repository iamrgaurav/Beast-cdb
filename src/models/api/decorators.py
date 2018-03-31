from functools import wraps
from flask import request, Response
from flask import request



def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token =None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X_API-KEY']
        if not token:
            return {'Error':'Token is Missing'},401

        return func(*args,**kwargs)
    return decorated


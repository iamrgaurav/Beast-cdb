from functools import wraps
from flask import request, Response
from flask import request

from src.models.api.api_user import Api_User


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


def check_auth(username, password):
    user = Api_User.is_login_valid(username,password)
    if user:
        return {'username':user.username}

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
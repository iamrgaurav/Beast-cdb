from flask_restplus import Api
from flask import Blueprint

from src.models.api.User.routes import user_namespace as user_ns
from src.models.api.dot.routes import admin_namespace as admin_ns

api_blueprint = Blueprint('api', __name__)

api = Api(
    api_blueprint,
    title='Beast API',
    version='1.0',
    description='Beaster',
)


api.add_namespace(user_ns, path='/user')
api.add_namespace(admin_ns, path='/dot-admin')
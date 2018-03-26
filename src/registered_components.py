from src.app import app
from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix = '/user')
from src.models.dot.views import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix = '/admin')

from src.models.api.api import api_blueprint
app.register_blueprint(api_blueprint, url_prefix = '/api')


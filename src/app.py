from flask import Flask
import os
from src.common.database import Database
import src.config as config
app = Flask(__name__)

app.config.from_object(config)
app.secret_key = os.environ.get('SECRET_KEY')


@app.before_first_request
def initialize_db():
    Database.initialize()

import src.route
import src.registered_components

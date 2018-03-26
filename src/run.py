from src.app import app
import src.config as AppConfig

app.run('localhost', 5000, AppConfig.DEBUG)
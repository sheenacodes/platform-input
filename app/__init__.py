from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)

from app import config
app.config.from_object(config.Config)
app.config.from_object(config.Configdb)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app)
from app import routes, models

from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/app/static", static_folder="static")
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models

import datetime, timeago


@app.template_filter("timeago")
def fromnow(date):
    return timeago.format(date, datetime.datetime.now())

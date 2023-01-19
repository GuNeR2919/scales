from flask import Blueprint
print('main\\__init__.py')

bp = Blueprint('main', __name__)

from app.main import routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from redis import Redis
import rq
from config import Config
print('app\\__init__.py')

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):
    print('call the create_app() function')
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('scales-task', connection=app.redis)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models

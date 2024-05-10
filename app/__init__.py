from flask import Flask
from .extensions import db
from .scheduler import init_scheduler
from .tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduler.db'
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    init_scheduler(app)

    app.register_blueprint(tasks_bp)

    return app

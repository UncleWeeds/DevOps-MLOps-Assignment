from datetime import datetime
from .extensions import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    execution_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recurrence = db.Column(db.String(50), nullable=True)
    def __repr__(self):
        return f'<Task {self.name}>'

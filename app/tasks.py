from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
from datetime import datetime
import random
from .scheduler import schedule_task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    execution_time = datetime.fromisoformat(data['execution_time'])
    recurrence = data.get('recurrence', None)
    new_task = Task(name=data['name'], execution_time=execution_time, recurrence=recurrence)
    db.session.add(new_task)
    db.session.commit()
    schedule_task(new_task.id, new_task.execution_time, recurrence)
    return jsonify({'message': 'Task created and scheduled successfully.'}), 201

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'name': task.name, 'execution_time': task.execution_time}
        output.append(task_data)
    return jsonify({'tasks': output}), 200

@tasks_bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({'name': task.name, 'execution_time': task.execution_time}), 200

@tasks_bp.route('/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    if 'execution_time' in data:
        task.execution_time = datetime.fromisoformat(data['execution_time'])
    if 'name' in data:
        task.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully.'}), 200

@tasks_bp.route('/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully.'}), 200

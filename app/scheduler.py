from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flask import current_app
import time
import random

def execute_task(app, task_id):
    with app.app_context():
        from .models import Task
        task = Task.query.get(task_id)
        if task:
            print(f"Executing task {task_id}: {task.name}")
            time_to_sleep = random.randint(1, 10)
            time.sleep(time_to_sleep)
            print(f"Task {task_id} completed. Slept for {time_to_sleep} seconds.")

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.start()

    app.config['SCHEDULER'] = scheduler
    app.config['APP_INSTANCE'] = app

    atexit.register(lambda: scheduler.shutdown())

def schedule_task(task_id, execution_time, recurrence=None):
    app = current_app.config.get('APP_INSTANCE')
    scheduler = current_app.config.get('SCHEDULER')

    if not scheduler or not app:
        print("Scheduler not initialized or found.")
        return

    job_id = f"task_{task_id}"

    if recurrence == 'daily':
        scheduler.add_job(
            execute_task,
            'interval',
            days=1,
            start_date=execution_time,
            args=[app, task_id],
            id=job_id,
            misfire_grace_time=15
        )
    elif recurrence == 'weekly':
        scheduler.add_job(
            execute_task,
            'interval',
            weeks=1,
            start_date=execution_time,
            args=[app, task_id],
            id=job_id,
            misfire_grace_time=15
        )
    elif recurrence:

        pass
    else:

        scheduler.add_job(
            execute_task,
            'date',
            run_date=execution_time,
            args=[app, task_id],
            id=job_id,
            misfire_grace_time=15
        )

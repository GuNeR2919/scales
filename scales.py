from app import create_app, db
from app.models import Weight, Task
from rq.registry import StartedJobRegistry
from rq.command import send_stop_job_command

print('scales.py')

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Weight': Weight, 'Task': Task}


registry = StartedJobRegistry('scales-task', connection=app.redis)
running_job_ids = registry.get_job_ids()
if running_job_ids:
    print(running_job_ids)
    send_stop_job_command(app.redis, running_job_ids[0])

# rq_job = app.task_queue.enqueue('app.scales_daemon.get_weight')
# task = Task(id=rq_job.get_id(), name='get_weight', description='ID of get_weight task')
# db.session.add(task)
# try:
#     with app.app_context():
#         running_task = Task.lunch_task()
#         registry = StartedJobRegistry('scales-task', connection=app.redis)
#         running_job_ids = registry.get_job_ids()
#         if running_job_ids:
#             print(running_job_ids)
# except KeyboardInterrupt:
#     registry = StartedJobRegistry('scales-task', connection=app.redis)
#     running_job_ids = registry.get_job_ids()
#     if running_job_ids:
#         print(running_job_ids)
#         send_stop_job_command(app.redis, running_job_ids[0])

from app import create_app, db
from app.models import Weight, Task
from rq.registry import StartedJobRegistry
from rq.command import send_stop_job_command

print('scales.py')

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Weight': Weight, 'Task': Task}


with app.app_context():
    registry = StartedJobRegistry('scales-task', connection=app.redis)
    running_job_ids = registry.get_job_ids()
    if running_job_ids:
        print('Stopping job:')
        print(*running_job_ids)
        send_stop_job_command(app.redis, running_job_ids[0])
    gwght_task = Task.launch_task()


# try:
#     with app.app_context():
#         gwght_task = Task.lunch_task(app.config['UUID'], )
#         registry = StartedJobRegistry('scales-task', connection=app.redis)
#         running_job_ids = registry.get_job_ids()
#         if running_job_ids:
#             print(running_job_ids)
#             print(gwght_task.get_rq_job())
# except KeyboardInterrupt:
#     registry = StartedJobRegistry('scales-task', connection=app.redis)
#     running_job_ids = registry.get_job_ids()
#     if running_job_ids:
#         print(running_job_ids)
#         send_stop_job_command(app.redis, running_job_ids[0])

from app import create_app, db
from app.models import Weight, Task

print('scales.py')

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Weight': Weight, 'Task': Task}


rq_job = app.task_queue.enqueue('app.scales_daemon.get_weight')

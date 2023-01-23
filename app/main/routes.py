from time import sleep
from datetime import datetime
# from flask_socketio import SocketIO
from flask import render_template, url_for, request, current_app
from app.models import Weight, Task
from app.main import bp
# from rq.registry import StartedJobRegistry
# from rq.command import send_stop_job_command

print('routes.py')

# socketio = SocketIO(app, async_mode=None, logger=False, engine_logger=False)


def get_weight(job):
    """
    Send current weight to client
    """
    wght = job.meta.get()
    print(f'Client: received weight is {wght}')
#    socketio.emit('weight', {'data': scales_daemon.weight})
    sleep(1)


@bp.route('/')
@bp.route('/index')
def index():
    # running_task = Task.lunch_task()
    # registry = StartedJobRegistry('scales-task', connection=current_app.redis)
    # running_job_ids = registry.get_job_ids()
    # if running_job_ids:
    #     print(running_job_ids)
    return render_template('index.html')


@bp.route('/weights')
def weights():
    page = request.args.get('page', 1, type=int)
    wght = Weight.query.order_by(
        Weight.mtime.desc()).paginate(
            page=page, per_page=current_app.config['WEIGHTS_PER_PAGE'],
            error_out=False)
    next_url = url_for('main.weights', page=wght.next_num) \
        if wght.has_next else None
    prev_url = url_for('main.weights', page=wght.prev_num) \
        if wght.has_prev else None
    for w in wght.items:
        w.mtime = datetime.utcfromtimestamp(w.mtime)
    return render_template('weights.html', title='Weights list',
                           weights=wght.items, next_url=next_url,
                           prev_url=prev_url)


# @socketio.on('connect')
# def test_connect():
#     print('Client connected')
#     print('Starting client thread')
#     socketio.start_background_task(get_weight)


# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

# running_task = Task.lunch_task()
# registry = StartedJobRegistry('scales-task', connection=current_app.redis)
# running_job_ids = registry.get_job_ids()
# if running_job_ids:
#     print(running_job_ids)

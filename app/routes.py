from time import sleep
from flask_socketio import SocketIO
from flask import render_template, url_for, request
from threading import Thread, Event
from app import app
from app import scales_daemon
from app.models import Weight
from datetime import datetime

app.config['SECRET_KEY'] = 'secret!wtf'
app.config['DEBUG'] = True

socketio = SocketIO(app, async_mode=None, logger=False, engine_logger=False)

thread = Thread()
thread_stop_event = Event()


def get_weight():
    """
    Send current weight to client
    """
    while not thread_stop_event.isSet():
        print(f'Client: received weight is {scales_daemon.weight}')
        socketio.emit('weight', {'data': scales_daemon.weight})
        sleep(1)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weights')
def weights():
    page = request.args.get('page', 1, type=int)
    weights = Weight.query.order_by(
        Weight.mtime.desc()).paginate(
            page=page, per_page=app.config['WEIGHTS_PER_PAGE'],
            error_out=False)
    next_url = url_for('weights', page=weights.next_num) \
        if weights.has_next else None
    prev_url = url_for('weights', page=weights.prev_num) \
        if weights.has_prev else None
    for w in weights.items:
        w.mtime = datetime.utcfromtimestamp(w.mtime)
    return render_template('weights.html', title='Weights list',
                           weights=weights.items, next_url=next_url,
                           prev_url=prev_url)


@socketio.on('connect')
def test_connect():
    global thread
    print('Client connected')
    if not thread.is_alive():
        print('Starting client thread')
        thread = socketio.start_background_task(get_weight)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

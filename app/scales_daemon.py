import socket
import re
from time import sleep
from app import db, create_app
from datetime import datetime
from app.models import Weight
from rq import get_current_job

app = create_app()
app.app_context().push()


def _set_got_weight(wght):
    job = get_current_job()
    if job:
        job.meta['weight'] = wght
        job.save_meta()


def close_scales_sock(sc_sock):
    sc_sock.close()
    wght = 'Connecting to scales...'
    sleep(2)
    print('Daemon: Close socket function call.')
    return False, wght


def smscl_weight(wght):
    wght = re.search(r'^[0|w]*([^0|\D]\d*)\skg', wght)
    if wght:
        if wght.group(1).isnumeric():
            wght = str(wght.group(1))
            return True, wght
    else:
        return False, 0


def bgscl_weight(wght):
    wght = re.search(r'(?<=\u000203)\d{6}', repr(wght))
    if wght:
        wght = re.search(r'[^0]\d*', repr(wght.group()))
        if wght.group().isnumeric():
            wght = str(wght.group())
            return True, wght


def get_weight():
    # global scales_con, weight
    time_stamp = 0
    weight_stamp = 0
    db_new = True
    scales_con = False
    scales_sock = None
    _set_got_weight('Connecting to the scales...')
    try:
        while True:
            if not scales_con:
                try:
                    scales_sock = \
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    scales_sock.connect((app.config['SCALES_HOST'],
                                         app.config['SCALES_PORT']))
                    scales_con = True
                except BaseException as msg:
                    print('Daemon: can\'t connect to the scales -', msg)
                    scales_con = False
            else:
                try:
                    weight_rcv = scales_sock.recv(51).decode('ascii')
                    if not weight_rcv:
                        _set_got_weight('Connecting to the scales ...')
                        scales_con, smwght = close_scales_sock(scales_sock)
                        continue
                    time_cur = int(datetime.now().timestamp())
                    time_pid = int(datetime.now().strftime("%y%m%d%H%M%S"))
                    print('Daemon: received -', weight_rcv)
                    smscl, smwght = smscl_weight(weight_rcv)
                    if smscl:
                        _set_got_weight(smwght)
                        if weight_stamp != smwght:
                            time_stamp = time_cur
                            weight_stamp = smwght
                            db_new = True
                            print('Daemon: time_stamp -', time_pid)
                        else:
                            if time_cur - time_stamp >= 15 and db_new:
                                weight_db = Weight(mtime=time_cur,
                                                   yard='jel1',
                                                   typ='',
                                                   weight=weight_stamp,
                                                   pid=time_pid)
                                with app.app_context():
                                    db.session.add(weight_db)
                                    db.session.commit()
                                    db_new = False
                                    print('Daemon: record added to DB')
                    else:
                        _set_got_weight(0)
                except BaseException as msg:
                    print('Daemon: received the error -', msg)
                    _set_got_weight('Connecting to the scales...')
                    scales_con, smwght = close_scales_sock(scales_sock)
                    continue
    except KeyboardInterrupt:
        close_scales_sock(scales_sock)
        print('Exit')
    print('Daemon function has stopped')

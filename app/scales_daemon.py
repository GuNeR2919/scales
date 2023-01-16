import socket
import re
from time import sleep
from app import app, db
from threading import Thread
from datetime import datetime
from app.models import Weight

scales_con = None
weight = None


def close_scales_sock(sc_sock):    # destroy scales socket function
    global scales_con, weight
    scales_con = False
    sc_sock.close()
    weight = 'Connecting to scales...'
    sleep(2)
    print('Daemon: Close socket function call.')


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
    global scales_con, weight
    time_stamp = 0
    weight_stamp = 0
    db_new = True
    scales_con = False
    scales_sock = None
    weight = 'Connecting to scales...'
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
                    print('Daemon: cant connect to scales -', msg)
                    scales_con = False
            else:
                try:
                    weight_rcv = scales_sock.recv(51).decode('ascii')
                    if not weight_rcv:
                        weight = 'Connecting to scales ...'
                        close_scales_sock(scales_sock)
                        continue
                    time_cur = int(datetime.now().timestamp())
                    time_pid = int(datetime.now().strftime("%y%m%d%H%M%S"))
                    print('Daemon: received -', weight_rcv)
                    smscl, smwght = smscl_weight(weight_rcv)
                    if smscl:
                        weight = smwght
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
                        weight = 0
                except BaseException as msg:
                    print('Daemon: received the error -', msg)
                    weight = 'Connecting to scales...'
                    close_scales_sock(scales_sock)
                    continue
    except KeyboardInterrupt:
        close_scales_sock(scales_sock)
        print('Exit')
    print('I got end of Daemon function')


th = Thread(target=get_weight)
th.daemon = True
th.start()

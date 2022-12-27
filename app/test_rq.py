import time
import random
import socket

HOST = '192.168.2.50'
PORT = 11001
scales_sock = None
scales_rq = "\x01\x13\x10"
scales_con = False
rq_sended = False
rq_rsv = ''

try:
    while True:
        if not scales_con:
            try:
                scales_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                scales_sock.connect((HOST, PORT))
                scales_con = True
            except BaseException as msg:
                print('Cant connect to scales -', msg)
                scales_con = False
                time.sleep(1)
        else:
            if not rq_sended:
                try:
                    scales_sock.sendall(scales_rq.encode('ascii'))
                    rq_sended = True
                    print('Request sended')
                except BaseException as msg:
                    print('Cant send request -', msg)
                    rq_sended = False
                    break
            else:
                try:
                    rq_rsv = scales_sock.recv(1024).decode('ascii')
                    print('Recieved str is -', rq_rsv)
                    time.sleep(1)
                    break
                except BaseException as msg:
                    print('Cant recieve answer -', msg)
                    time.sleep(1)
                    continue
    scales_sock.close()
except KeyboardInterrupt :
    scales_sock.close()

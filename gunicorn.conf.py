import multiprocessing

bind = "0.0.0.0:5000"
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 4
timeout = 30

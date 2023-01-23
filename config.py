import os
from uuid import uuid4
from datetime import datetime

print('config.py')

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
#    'mysql+pymysql://scales:\'%zN.n3S\@IEc=Djx@192.168.6.136:3306/scales'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEIGHTS_PER_PAGE = 10
    SCALES_HOST = '192.168.6.18'
    SCALES_PORT = 11001
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://192.168.6.136'
    UUID = uuid4()
    TIMEST = datetime.now().timestamp()

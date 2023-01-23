import redis
import rq
from flask import current_app
from app import db
from rq.command import send_stop_job_command

print('models.py')


class Weight(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    mtime = db.Column(db.Integer, index=True, unique=True)
    yard = db.Column(db.String(8), index=True)
    rbook = db.Column(db.Integer())
    typ = db.Column(db.String(1))
    weight = db.Column(db.Integer)
    pid = db.Column(db.String(12))

    def __repr__(self):
        return '<Weight {}>'.format(self.weight)


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    print('Class Task created')
    # main_process_id = db.Column(db.String(128), index=True)
    # timestamp = db.Column(db.Integer())

    @staticmethod
    def launch_task():
        rq_job = current_app.task_queue.enqueue('app.scales_daemon.get_weight')
        task = Task(id=rq_job.get_id())
        db.session.add(task)
        db.session.commit()
        return task

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_weight(self):
        job = self.get_rq_job()
        job.refresh()
        return job.meta if job is not None else 0

    def stop_task(self):
        send_stop_job_command(current_app.redis, self.id)

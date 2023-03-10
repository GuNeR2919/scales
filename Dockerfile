FROM python:slim

RUN useradd scales

WORKDIR /home/scales

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install pyparsing pyproject.toml wheel
RUN venv/bin/pip install gunicorn[gevent]
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY scales.py config.py boot.sh gunicorn.conf.py ./
RUN chmod +x boot.sh

ENV FLASK_APP scales.py

RUN chown -R scales:scales ./
USER scales

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

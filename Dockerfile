FROM python:3.8-slim
LABEL maintainer="s1mplecc <s1mple951205@gmail.com>"
LABEL description="Website external link crawer, providing Restful API service."

ENV FLASK_WORK_DIR="/root/flask"

EXPOSE 8000

WORKDIR $FLASK_WORK_DIR

COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn gevent
RUN chmod +x gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]
FROM python:3.8-slim
LABEL description="Docker image with Spark (3.1.2) and Hadoop (3.2.0), based on bitnami/spark:3. \
For more information, please visit https://github.com/s1mplecc/spark-hadoop-docker."

ENV FLASK_WORK_DIR="/root/flask"

EXPOSE 8000

WORKDIR $FLASK_WORK_DIR

COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN chmod +x gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]
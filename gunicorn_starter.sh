#!/bin/sh
gunicorn --worker-class=gevent --worker-connections=1000 -w 4 -b 0.0.0.0:8000 app:app
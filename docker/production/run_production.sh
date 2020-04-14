#!/bin/bash

NAME='votes-service'
APP='votes:create_app()'
NUM_WORKERS=5
PORT=":8080"

export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn $APP \
    --name $NAME \
    --workers $NUM_WORKERS \
    --log-level=debug \
    -b $PORT \
    --capture-output

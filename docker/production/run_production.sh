#!/bin/bash

PYTHONDIR="/app"
NAME='votes-service'
APP='votes:create_app()'
NUM_WORKERS=5
PORT=":8080"

export PYTHONPATH=$PYTHONDIR
export FLASK_APP=votes
export FLASK_ENV=production

exec gunicorn $APP \
    --name $NAME \
    --workers $NUM_WORKERS \
    --log-level=debug \
    -b $PORT \
    --capture-output

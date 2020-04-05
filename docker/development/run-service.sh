#!/bin/sh

set -e

pip install -r requirements/local.txt

export FLASK_APP=votes
export FLASK_ENV=development

exec flask run -h 0.0.0.0 -p 8000

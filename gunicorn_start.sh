#!/usr/bin/env bash

# Default port 5000 if unset env variable.
if [ -z ${PORT+x} ]; then PORT=5000; else echo "PORT is set to '$PORT'"; fi

gunicorn --bind 0.0.0.0:$PORT \
  --bind unix:/app/conda_parser.sock \
  --error-logfile - \
  --timeout=3600\
  -w 2 --threads 4 \
  conda_parser.wsgi:app

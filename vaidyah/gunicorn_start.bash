#!/bin/bash

NAME="vaidyah"                                   # Name of the application
DJANGODIR=/home/martial/diseno/webpy/vaidyah        # Django project directory
SOCKFILE=/home/martial/diseno/webpy/venv/run/gunicorn.sock  # we will communicte using this unix socket
USER=martial                                         # the user to run as
GROUP=martial                                        # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=vaidyah.settings            # which settings file should Django use
DJANGO_WSGI_MODULE=vaidyah.wsgi                # WSGI module name
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR
source /home/martial/diseno/webpy/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
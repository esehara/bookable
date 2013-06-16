#/bin/bash
source $BOOKABLE_VIRTUALENV_PATH
cd $BOOKABLE_ROOT
gunicorn bookable.wsgi:application -b 0.0.0.0:8088

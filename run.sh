#/bin/bash
source $HOME/env/bookable.sh
source $BOOKABLE_VIRTUALENV_PATH
cd $BOOKABLE_ROOT
gunicorn bookable.wsgi:application -c gunicorn.ini

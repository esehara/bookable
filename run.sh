#/bin/bash
source $BOOKABLE_VIRTUALENV_PATH
cd $BOOKABLE_ROOT
python manage.py run_gunicorn -b 0.0.0.0:8088

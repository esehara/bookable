# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
from fabric.api import *


@hosts(
    '%s:%s' %
    (os.environ['BOOKABLE_HOST'],
    os.environ['BOOKABLE_PORT']))
def deploy():
    # TODO: bad how-to
    with cd('~/django/bookable'):
        run('git reset --hard')
        run('git pull origin master')
        run('source ~/env/bookable/bin/activate &&'
            'source ~/env/bookable.sh &&'
            'pip install -r requirement.txt &&'
            'python manage.py migrate',
            shell=False)
    supervisorctl()


def supervisorctl():
    sudo('pkill -f supervisord')
    sudo('pkill -f gunicorn')
    sudo('supervisord')

#! /bin/bash
sudo pkill -f supervisord
sudo pkill -f gunicorn
sudo supervisord

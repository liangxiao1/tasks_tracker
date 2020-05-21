# Task Tracker Quick Start

Simple application shows the tasks.

## Clone the repo

    git clone https://github.com/liangxiao1/tasks_tracker.git

## Swith to repo directory and install required pkgs

    cd tasks_tracker
    pip install -r requirements.txt

## Create an Admin user(only required at first run)

    flask fab create-admin

## Start the app

    flask run -h 0.0.0.0 -p 5000

## Access it via below link

    http://$ip:5000

## References

### - *[Flask-AppBuilder](https://flask-appbuilder.readthedocs.io/en/latest/index.html)*

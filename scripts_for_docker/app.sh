#!/bin/bash

cd app

alembic upgrade head

alembic upgrade head

gunicorn main:application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
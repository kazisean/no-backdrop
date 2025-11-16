#!/bin/bash
cd /app
celery -A celery_worker worker --loglevel=info --pool=prefork --concurrency=4
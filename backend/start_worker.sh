#!/bin/bash
cd /app
exec celery -A app.celery_worker worker \
    --loglevel=info \
    --pool=solo \
    --max-memory-per-child=1048576 \
    --max-tasks-per-child=10 \
    --without-gossip \
    --without-mingle \
    --without-heartbeat
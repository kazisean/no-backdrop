#!/bin/bash
cd /app
exec celery -A celery_worker worker \
    --loglevel=info \
    --pool=solo \
    --max-memory-per-child=524288 \
    --without-gossip \
    --without-mingle \
    --without-heartbeat
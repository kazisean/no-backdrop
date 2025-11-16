#!/bin/bash
cd /app
exec celery -A celery_worker worker \
    --loglevel=info \
    --pool=prefork \
    --concurrency=2 \
    --max-memory-per-child=1048576 \
    --without-gossip \
    --without-mingle
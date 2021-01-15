#!/bin/sh

set -e

while ! poetry run alembic -c billing/alembic/alembic.ini --raiseerr upgrade heads
do
     echo "Retry..."
     sleep 1
done

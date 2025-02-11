#!/usr/bin/env bash
   set -e  # Exit on error

   # 1. Run migrations
   poetry run alembic upgrade head

   # 2. Then launch your web server (whatever your usual CMD is)
   exec "$@"
#!/bin/sh

PYTHONPATH=.:libs/requests PM_PREFS_PATH=~/.package_backup.dev PM_API_URL_PREFIX='http://localhost:8080' pbclient/tools/pb_pushlist_dpkg.py


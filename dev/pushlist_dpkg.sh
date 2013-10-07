#!/bin/sh

PB_PREFS_PATH=~/.package_backup.dev PB_API_URL_PREFIX=http://localhost:8080 PYTHONPATH=.:../pysecure pbclient/tools/pb_pushlist_dpkg.py


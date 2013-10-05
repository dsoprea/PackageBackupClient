#!/bin/sh

PM_PREFS_PATH=~/.package_backup.dev PM_API_URL_PREFIX=http://localhost:8080 PYTHONPATH=.:../pysecure pmclient/tools/pm_pushlist_dpkg.py


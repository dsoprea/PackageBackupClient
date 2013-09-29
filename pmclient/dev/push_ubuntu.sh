#!/bin/sh

PYTHONPATH=.:libs/requests PM_API_URL_PREFIX='http://localhost:8080' pmclient/tools/pm_push_dpkg.py


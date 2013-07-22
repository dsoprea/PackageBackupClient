#!/usr/bin/python

from sys import exit, path
path.insert(0, '.')

from snackwich.main import Snackwich

from p_m.tools.data.pm_config_snack import config
from p_m.prefs import Prefs

panels = Snackwich(config)

result = panels.execute('window1')

if result is None:
    print("Interactive configuration cancelled.\n")
    exit(1)
    
values = result['window1']['values']

prefs_ = { 'system_name': values[0],
           'api_key': values[1],
           'api_secret': values[2] }

prefs = Prefs()
prefs.initialize(prefs_)

prefs.save()

print("Preferences saved.")


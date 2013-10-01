#!/usr/bin/python3

from sys import exit, path
path.insert(0, '.')

from snackwich.main import Snackwich

from pmclient.tools.data.pm_config_snack import config
from pmclient.prefs import Prefs

def start_config():
    panels = Snackwich(config)

    result = panels.execute('window1')

    if result is None:
        print("Interactive configuration cancelled.\n")
        exit(1)
        
    values = result['window1']['values']

    prefs_ = { 'system_name': values[0],
               'api_key': values[1],
               'api_secret': values[2],
               
    # TODO: Fill these in when we expose the functionality.
               'backup_agent_class': '',
               'backup_agent_json_file': '' 
               }

    prefs = Prefs()
    prefs.initialize(prefs_)

    prefs.save()

    print("Preferences saved.")

if __name__ == '__main__':
    start_config()


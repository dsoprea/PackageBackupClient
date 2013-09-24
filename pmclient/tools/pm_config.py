#!/usr/bin/python3

from sys import exit, path
path.insert(0, '.')

from argparse import ArgumentParser

from pmclient.prefs import Prefs

description = "Write the current user's Package Monitor configuration."

parser = ArgumentParser(description=description)
mutex = parser.add_mutually_exclusive_group(required=True)

mutex.add_argument('--set-initial', 
                   nargs=5, 
                   metavar=('system_name', 'key', 'secret', 
                            'backup_agent_class', 'backup_agent_json_file'), 
                   help="Set [initial] configuration.")

mutex.add_argument('--set-system-name', 
                   nargs=1, 
                   metavar=('system_name'), 
                   help="Set system-name.")

mutex.add_argument('--set-creds', 
                   nargs=2, 
                   metavar=('key', 'secret'), 
                   help="Set API credentials.")

mutex.add_argument('--set-backup-agent', 
                   nargs=2, 
                   metavar=('class', 'json_file'), 
                   help="Set backup-agent info.")

mutex.add_argument('--display', 
                   action='store_true', 
                   help="Display stored preferences.")

result = parser.parse_args()

prefs = Prefs()

def load_prefs():
    try:
        prefs.load()
    except Exception as e:
        if prefs.exists() is False:
            print("Can not load current configuration. It does not exist.")
            exit(1)
        else:
            print("Can not load current configuration: %s" % (str(e)))
            exit(2)

if result.set_initial:
    prefs_ = { 'system_name': result.set_initial[0],
               'api_key': result.set_initial[1],
               'api_secret': result.set_initial[2],
               'backup_agent_class': result.set_initial[3],
               'backup_agent_json_file': result.set_initial[4] }

    prefs = Prefs()
    prefs.initialize(prefs_)

    prefs.save()

    print("Preferences saved.")
elif result.set_system_name:
    load_prefs()
    
    prefs.set('system_name', result.set_system_name[0])
    prefs.save()

    print("System name updated.")
elif result.set_creds:
    load_prefs()

    prefs.set('api_key', result.set_creds[0])
    prefs.set('api_secret', result.set_creds[1])
    prefs.save()

    print("Credentials updated.")
elif result.set_backup_agent:
    load_prefs()

    prefs.set('backup_agent_class', result.set_backup_agent[0])
    prefs.set('backup_agent_json_file', result.set_backup_agent[1])
    prefs.save()

    print("Backup-agent updated.")
elif result.display:
    load_prefs()

    for k, v in prefs.get_dict().items():
        print("%s: %s" % (k, v))


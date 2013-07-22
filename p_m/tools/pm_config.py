#!/usr/bin/python3

from sys import exit
from argparse import ArgumentParser

from p_m.prefs import Prefs

description = "Write the current user's Package Monitor configuration."

parser = ArgumentParser(description=description)
mutex = parser.add_mutually_exclusive_group(required=True)

mutex.add_argument('--set-initial', nargs=3, metavar=('system_name', 'key', 'secret'), 
                   help="Set [initial] configuration.")
mutex.add_argument('--set-system-name', nargs=1, metavar=('system_name'), 
                   help="Set system-name.")
mutex.add_argument('--set-creds', nargs=2, metavar=('key', 'secret'), 
                   help="Set API credentials.")
mutex.add_argument('--display', action='store_true', help="Display stored preferences.")

result = parser.parse_args()

prefs = Prefs()

if result.set_initial:
    prefs_ = { 'system_name': result.set_initial[0],
               'api_key': result.set_initial[1],
               'api_secret': result.set_initial[2] }

    prefs = Prefs()
    prefs.initialize(prefs_)

    prefs.save()

    print("Preferences saved.")
elif result.set_system_name:
    try:
        prefs.load()
    except:
        if prefs.exists():
            print("Can not load current configuration. It does not exist.")
            exit(1)
        else:
            print("Can not load current configuration. There was an error.")
            exit(2)
    
    prefs.set('system_name', result.set_system_name[0])
    prefs.save()

    print("Preferences saved.")
elif result.set_creds:
    try:
        prefs.load()
    except:
        if prefs.exists():
            print("Can not load current configuration. It does not exist. (2)")
            exit(3)
        else:
            print("Can not load current configuration. There was an error. (2)")
            exit(4)

    prefs.set('api_key', result.set_creds[0])
    prefs.set('api_secret', result.set_creds[1])
    prefs.save()

    print("Preferences saved.")
elif result.display:
    try:
        prefs.load()
    except:
        if prefs.exists():
            print("Can not load current configuration. It does not exist. (3)")
            exit(5)
        else:
            print("Can not load current configuration. There was an error. (3)")
            exit(6)

    for k, v in prefs.get_dict().items():
        print("%s: %s" % (k, v))


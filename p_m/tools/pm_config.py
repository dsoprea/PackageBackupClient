#!/usr/bin/python

from sys import exit
from argparse import ArgumentParser

from p_m.prefs import Prefs

description = "Write the current user's Package Monitor configuration."

parser = ArgumentParser(description=description)
mutex = parser.add_mutually_exclusive_group(required=True)

mutex.add_argument('--set', nargs=2, metavar=('key', 'secret'), 
                   help="Set the API credentials.")
mutex.add_argument('--display', action='store_true', help="Display stored preferences.")

result = parser.parse_args()

if result.set:
    prefs_ = { 'api_key': result.set[0],
               'api_secret': result.set[1] }

    prefs = Prefs()
    prefs.initialize(prefs_)

    prefs.save()

    print("Preferences saved.")

elif result.display:
    prefs = Prefs()
    prefs.load()

    for k, v in prefs.get_dict().iteritems():
        print("%s: %s" % (k, v))


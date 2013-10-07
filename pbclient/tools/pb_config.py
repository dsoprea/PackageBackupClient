#!/usr/bin/python3

from sys import exit, path
path.insert(0, '.')

from argparse import ArgumentParser

from pbclient.prefs import Prefs

def start_config():
    Prefs().load_from_console()

if __name__ == '__main__':
    description = "Modify the current user's Package Backup configuration."

    parser = ArgumentParser(description=description)

    parser.add_argument('--display', 
                        action='store_true', 
                        help="Display stored preferences.")

    result = parser.parse_args()


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

    if result.display:
        load_prefs()

        for k, v in prefs.get_dict().items():
            print("%s: %s" % (k, v))

        exit(0)

    start_config()


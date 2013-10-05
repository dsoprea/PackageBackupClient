import logging

from argparse import ArgumentParser

from pmclient.client import Client

def push_list(system_profiler, package_list_getter):
    parser = ArgumentParser(description='Package-list push for DPKG.')
    parser.add_argument('-v', '--verbose', action='store_true', help="Show logging.")

    result = parser.parse_args()

    if result.verbose:
        from pmclient import logging_config

    # Gather data.

    package_list = package_list_getter().get_package_list()

    try:
        Client(system_profiler).list_push(package_list)
    except Exception as e:
        logging.exception("There was a problem pushing.")
        exit(1)

    print("Push successful.")
    exit(0)


import logging

from argparse import ArgumentParser

from pmclient.constants.http import HTTP_METHOD_ALREADY_EXISTS
from pmclient.exceptions.http import HttpRequestError
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
    except HttpRequestError as e:
        if e.code == HTTP_METHOD_ALREADY_EXISTS:
            print("List has already been pushed for today.\n")
            exit(2)

    print("Push successful.")
    exit(0)


#!/usr/bin/python3

from sys import exit
from argparse import ArgumentParser

from p_m.system.system_types import get_system_imps, SYS_ARCH
from p_m.system.repo_types import get_repo_imps, SYS_PACMAN
from p_m.client import Client

parser = ArgumentParser(description='Package-list push for DPKG.')
parser.add_argument('-v', '--verbose', action='store_true', help="Show logging.")

result = parser.parse_args()

if result.verbose:
    from p_m import logging_config

system_profiler = get_system_imps(SYS_ARCH)
package_list_getter = get_repo_imps(SYS_PACMAN)

# Gather data.

system_info = system_profiler().get_system_info()
package_list = package_list_getter().get_package_list()

try:
    Client().list_push(system_info, package_list)
except Exception as e:
    logging.exception("There was a problem pushing.")
    exit(1)

exit(0)


#!/usr/bin/python

from sys import exit

from p_m.system.system_types import get_system_imps, SYS_UBUNTU
from p_m.system.repo_types import get_repo_imps, SYS_APT
from p_m.client import Client

system_profiler = get_system_imps(SYS_UBUNTU)
package_list_getter = get_repo_imps(SYS_APT)

# Gather data.

system_info = system_profiler().get_system_info()
package_list = package_list_getter().get_package_list()

Client().list_push(system_info, package_list)

exit(0)


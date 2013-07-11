#!/usr/bin/python

from sys import exit

from p_m.system.system_specific import get_system_imps, SYS_UBUNTU
from p_m.client import Client

(system_profiler, package_list_getter) = get_system_imps(SYS_UBUNTU)

# Gather data.

system_info = system_profiler().get_system_info()
package_list = package_list_getter().get_package_list()

Client().list_push(system_info, package_list)

exit(0)


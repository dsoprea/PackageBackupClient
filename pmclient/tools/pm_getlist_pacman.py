#!/usr/bin/python3

from sys import exit, path
path.insert(0, '.')

from pmclient.tools.base.get_list import render_list_info
from pmclient.system.system_types import get_system_imps, SYS_ARCH

if __name__ == '__main__':
    system_profiler = get_system_imps(SYS_ARCH)
    render_list_info(system_profiler)


#!/usr/bin/env python3.3

from sys import exit, path
path.insert(0, '.')

from pbclient.tools.base.push_list import push_list
from pbclient.system.system_types import get_system_imps, SYS_ARCH
from pbclient.system.repo_types import get_repo_imps, SYS_PACMAN

if __name__ == '__main__':
    system_profiler = get_system_imps(SYS_ARCH)
    package_list_getter = get_repo_imps(SYS_PACMAN)

    push_list(system_profiler, package_list_getter)


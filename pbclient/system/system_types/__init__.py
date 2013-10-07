from pbclient.system.system_types import ubuntu, arch

SYS_UBUNTU = 'ubuntu'
SYS_ARCH = 'arch'

_systems = { SYS_UBUNTU: ubuntu.imp,
             SYS_ARCH: arch.imp }

def get_system_imps(type_):
    return _systems[type_]


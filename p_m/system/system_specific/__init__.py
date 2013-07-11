from p_m.system.system_specific import ubuntu

SYS_UBUNTU = 'ubuntu'

_systems = { SYS_UBUNTU: ubuntu.imp }

def get_system_imps(type_):
    return _systems[type_]


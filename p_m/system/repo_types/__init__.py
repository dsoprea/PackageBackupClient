from p_m.system.system_specific import apt, pacman

SYS_APT = 'apt'
SYS_PACMAN = 'pacman'

_repos = { SYS_APT: apt.imp,
           SYS_PACMAN: pacman.imp }

def get_repo_imps(type_):
    return _repos[type_]


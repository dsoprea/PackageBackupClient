from pbclient.system.repo_types import dpkg, pacman

SYS_DPKG = 'dpkg'
SYS_PACMAN = 'pacman'

_repos = { SYS_DPKG: dpkg.imp,
           SYS_PACMAN: pacman.imp }

def get_repo_imps(type_):
    return _repos[type_]


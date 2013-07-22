from subprocess import Popen, PIPE

from p_m.interfaces.system_specific.ipackage_list_getter \
    import IPackageListGetter
from p_m.interfaces.system_specific.isystem_profiler \
    import ISystemProfiler
from p_m.system.system_info import SystemInfo


# TODO: Refactor for Arch.
class ArchSystemProfiler(ISystemProfiler):
    def __info_getter(self, argument):
        command = ['lsb_release', argument]
        p = Popen(command, stdout=PIPE)
        result = p.communicate()[0].decode('ASCII')
        
        if p.returncode != 0:
            raise Exception("Could not get system info with argument ['%s']." % 
                            (argument))
    
        starts_at = (result.index(':') + 1)
        return result[starts_at:].strip()
    
    def get_system_info(self):

        repo_type = 'pacman'
        os_type = self.__info_getter('-i')
        os_version = self.__info_getter('-r')
        
        return SystemInfo(repo_type, os_type, os_version)

imp = ArchSystemProfiler


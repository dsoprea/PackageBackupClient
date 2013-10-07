from subprocess import Popen, PIPE

from pbclient.interfaces.system_specific.ipackage_list_getter \
    import IPackageListGetter


# TODO: Refactor for Pacman.
class PacmanPackageListGetter(IPackageListGetter):
    def get_package_list(self):
        """Get the list of packages in whatever format the user will need to 
        restore the packages.
        """

        command = ['pacman', '-Qqen']
        p = Popen(command, stdout=PIPE)
        list_data = p.communicate()[0]

        if p.returncode != 0:
            raise Exception("The 'pacman' package-list call returned error "
                            "(%d)." % (p.returncode))

        return list_data

imp = PacmanPackageListGetter


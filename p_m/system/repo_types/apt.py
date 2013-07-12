from subprocess import Popen, PIPE

from p_m.interfaces.system_specific.ipackage_list_getter \
    import IPackageListGetter


class AptPackageListGetter(IPackageListGetter):
    def get_package_list(self):
        """Get the list of packages in whatever format the user will need to 
        restore the packages.
        """

        command = ['dpkg', '--get-selections']
        p = Popen(command, stdout=PIPE)
        list_data = p.communicate()[0]

        if p.returncode != 0:
            raise Exception("The package-list call returned error (%d)." % 
                            (p.returncode))

        return list_data

imp = AptPackageListGetter


class IPackageListGetter(object):
    def get_package_list(self):
        """Get the list of packages in whatever format the user will need to 
        restore the packages. Returns a string.
        """

        raise NotImplementedError()


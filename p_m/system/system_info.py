class SystemInfo(object):
    def __init__(self, repo_type, os_type, os_version):
        self.__repo_type = repo_type
        self.__os_type = os_type
        self.__os_version = os_version

    def __repr__(self):
        return ('<SYSTEM-INFO RT=[%s] OT=[%s] OV=[%s]>' % 
                (self.__repo_type, self.__os_type, self.__os_version))

    @property
    def repo_type(self):
        return self.__repo_type

    @property
    def os_type(self):
        return self.__os_type

    @property
    def os_version(self):
        return self.__os_version


class SystemInfo(object):
    __repo_type_max_len = 20
    __os_type_max_len = 30
    __os_version_max_len = 10

    def __init__(self, repo_type, os_type, os_version):
        self.__repo_type = repo_type[:self.__class__.__repo_type_max_len]
        self.__os_type = os_type[:self.__class__.__os_type_max_len]
        self.__os_version = str(os_version)[:self.__class__.__os_version_max_len]

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


class IBackupClient(object):
    def remote_recent(self, max_days, descending=True):
        raise NotImplementedError()

    def get(self, path_to, filename):
        raise NotImplementedError()

    def put(self, path_from, filename):
        raise NotImplementedError()

    def delete(self, filename):
        raise NotImplementedError()


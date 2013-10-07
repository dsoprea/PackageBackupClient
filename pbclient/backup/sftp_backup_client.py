from pysecure.easy import EasySsh
from pysecure.adapters.sftpa import SftpFile

from pbclient.backup.ibackup_client import IBackupClient

class SftpBackupClient(IBackupClient):
    def __init__(self, user, host, auth_cb, remote_path, allow_new=True):
        self.__easy = EasySsh(user, host, auth_cb, allow_new)

        self.__easy.open_ssh()
        self.__easy.open_sftp()

        self.__remote_path = remote_path

    def list_recent(self, max_items, descending=True):
        entries_raw = self.__easy.sftp.listdir(self.__remote_path, 
                                               get_directories=False)

        entries = sorted(entries_raw, 
                         key=lambda e: e.modified_time, 
                         reverse=True)

        return entries[0:max_items]

    def get(self, filename, path_to):
        filepath_from = ('%s/%s' % (self.__remote_path, filename))
        filepath_to = ('%s/%s' % (path_to, filename))

        self.__easy.sftp.write_to_local(filepath_from, filepath_to)

    def put(self, path_from, filename):
        filepath_from = ('%s/%s' % (path_from, filename))
        filepath_to = ('%s/%s' % (self.__remote_path, filename))

        self.__easy.sftp.write_to_remote(filepath_from, filepath_to)

    def delete(self, filename):
        file_path = ('%s/%s' % (self.__remote_path, filename))

        self.__easy.sftp.unlink(file_path)

    @property
    def easy(self):
        return self.__easy


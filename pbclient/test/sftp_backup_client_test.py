from unittest import TestCase
from os import mkdir
from os.path import basename, dirname

from pysecure.easy import get_key_auth_cb
from pysecure.exceptions import SftpAlreadyExistsError
from pysecure import log_config

from pbclient.backup.sftp_backup_client import SftpBackupClient
from pbclient.test.test_config import user, host, key_filepath, \
                                      remote_backup_path

local_test_file_path = '/home/dustin/Pictures/IMG_1381.JPG'

local_test_path = dirname(local_test_file_path)
local_test_filename = basename(local_test_file_path)
local_test_write_path = '/tmp'


class SftpBackupClientTest(TestCase):
    def setUp(self):
        auth_cb = get_key_auth_cb(key_filepath)

        self.__client = SftpBackupClient(user, host, auth_cb, 
                                         remote_backup_path)
    
        try:
            self.__client.easy.sftp.mkdir('/tmp/backup_deposit')
        except SftpAlreadyExistsError:
            pass
    
    def tearDown(self):
        self.__client = None

    def test_list_recent(self):
        self.__client.list_recent(5)

    def test_get(self):
        self.__client.put(local_test_path, local_test_filename)
        self.__client.get(local_test_filename, local_test_write_path)

    def test_put(self):
        self.__client.put(local_test_path, local_test_filename)

    def test_delete(self):
        self.__client.put(local_test_path, local_test_filename)
        self.__client.delete(local_test_filename)



#import base64
#import getpass
#import os
#import socket
#import sys
#import traceback

#import paramiko

from os.path import expanduser 
from paramiko import SFTPClient, Transport
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.util import load_host_keys

KT_DSA = 'key_dsa'
KT_RSA = 'key_rsa'


class SftpClient(object):
    """Supported calls:

def close(self):
def listdir(self, path='.'):
def listdir_attr(self, path='.'):
def open(self, filename, mode='r', bufsize=-1):
def remove(self, path):
def rename(self, oldpath, newpath):
def mkdir(self, path, mode=0777):
def rmdir(self, path):
def stat(self, path):
def lstat(self, path):
def symlink(self, source, dest):
def chmod(self, path, mode):
def chown(self, path, uid, gid):
def utime(self, path, times):
def truncate(self, path, size):
def readlink(self, path):
def normalize(self, path):
def chdir(self, path):
def getcwd(self):
def putfo(self, fl, remotepath, file_size=0, callback=None, confirm=True):
def put(self, localpath, remotepath, callback=None, confirm=True):
def getfo(self, remotepath, fl, callback=None):
def get(self, remotepath, localpath, callback=None):
"""

    def __init__(self, hostname, username, \
                 client_key_filepath='~/.ssh/id_dsa', client_key_type=KT_DSA, \
                 client_passphrase=None, server_key=None, port=22):
        """Initialize the SFTP adapter."""

        client_key_filepath = expanduser(client_key_filepath)
        print(client_key_filepath)

        if client_key_type == KT_DSA:
            print("Using DSA key.")
            client_key = DSSKey.from_private_key_file(client_key_filepath, \
                                                      client_passphrase)
        elif client_key_type == KT_RSA:
            print("Using RSA key.")
            client_key = RSAKey.from_private_key_file(client_key_filepath, \
                                                      client_passphrase)
        else:
            raise Exception("Client key-type [%s] is not valid." % 
                            (client_key_type))

        self.__hostname = hostname
        self.__username = username
        self.__client_key = client_key
        self.__server_key = server_key
        self.__port = port

    def __get_host_key_info(self, hostname, allow_missing=True):
        host_key_file = expanduser('~/.ssh/known_hosts')
#        print(host_key_file)
        
#        from paramiko.util import log_to_file
#        log_to_file('/tmp/paramiko.log')
        
        try:
            all_host_keys = load_host_keys(host_key_file)
        except IOError:
            if allow_missing is False:
                raise

            all_host_keys = {}

#        all_host_keys.lookup('dustinplex')

        from base64 import b64decode

        salt_encoded = 'm9I3pi6j1bDPmu4U7kVNHzvqt0Q='
        host = 'dustinplex'
        host_hash = b64decode('ZExXObfhVvuh2UPO2QwcklZ7Ko8=')
        print(all_host_keys.__class__.hash_host(host, salt=salt_encoded))

#        all_host_keys.add('dustinplex', 'ssh-rsa', 'xyz')
#ecdsa-sha2-nistp256

#        print("Looking-up: %s" % (all_host_keys.lookup('dustinplex')))
        from sys import exit
        exit()

#        from pprint import pprint
#        print('HASHED: ' + all_host_keys.__class__.hash_host('dustinplex'))

#        print("Checking.")
        
#        print(all_host_keys.keys())
        
#        host_keys = all_host_keys['dustinplex']
#        print("Result:\n%s" % (host_keys))

        try:
            host_keys = all_host_keys[hostname]
        except KeyError:
            return (None, None)
        else:
            host_key_type = host_keys.keys()[0]
            host_key = host_keys[host_key_type]

            return (host_key_type, host_key)

    def __enter__(self, allow_missing_host_key=True):
        print("Creating transport.")
        self.__t = Transport((self.__hostname, self.__port))

        (hk_type, hk) = self.__get_host_key_info(self.__hostname, 
                                                 allow_missing_host_key)

#        print("Host-key: %s" % (hk))
 
        def hk(allowed_types):
            print("Allowed types: %s" % (allowed_types,))
            print("Server key: %s" % (str(self.__t.get_remote_server_key().__class__)))

            return 'ssh-dss'#ecdsa-sha2-nistp256

        print("Connecting %s@%s." % (self.__username, self.__hostname))
        self.__t.connect(username=self.__username, 
                         pkey=self.__client_key, 
                         hostkey=hk)

# TODO: Finish implementing this.
#                         hostkey=self.__server_key)

        self.__sftp = SFTPClient.from_transport(self.__t)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__t.close()

        if exc_type is not None:
            return

    def __getattr__(self, name):
        return getattr(self.__sftp, name)

hostname = 'dustinplex'
username = 'dustin'
pkey_filepath = '/home/dustin/.ssh/id_rsa'

with SftpClient(hostname, username, client_key_filepath=pkey_filepath, \
                client_key_type=KT_RSA) as s:

    print("Listing entries.")
    entries = s.listdir_attr('.')

    for entry in entries:
        print(entry)
#        print("%s\n%s" % (entry.filename, entry))

#    dirlist = sftp.listdir('.')
#    print "Dirlist:", dirlist
#
#    # copy this demo onto the server
#    try:
#        sftp.mkdir("demo_sftp_folder")
#    except IOError:
#        print '(assuming demo_sftp_folder/ already exists)'
#    sftp.open('demo_sftp_folder/README', 'w').write('This was created by demo_sftp.py.\n')
#    data = open('demo_sftp.py', 'r').read()
#    sftp.open('demo_sftp_folder/demo_sftp.py', 'w').write(data)
#    print 'created demo_sftp_folder/ on the server'
#
#    # copy the README back here
#    data = sftp.open('demo_sftp_folder/README', 'r').read()
#    open('README_demo_sftp', 'w').write(data)
#    print 'copied README back here'
#
#    # BETTER: use the get() and put() methods
#    sftp.put('demo_sftp.py', 'demo_sftp_folder/demo_sftp.py')
#    sftp.get('demo_sftp_folder/README', 'README_demo_sftp')



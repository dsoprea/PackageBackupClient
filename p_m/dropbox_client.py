#import locale

from sys import exit
from os import path, unlink
#from pprint import pprint

from dropbox.client import DropboxClient, DropboxOAuth2FlowNoRedirect
from dropbox.rest import ErrorResponse

from p_m.config import DROPBOX_APP_KEY, DROPBOX_APP_SECRET
#DROPBOX_APP_KEY = ''
#DROPBOX_APP_SECRET = ''


class DbException(Exception):
    pass

class DbNeedsLoginException(DbException):
    pass

def _secure():
    """a decorator for handling authentication and exceptions"""
    def decorate(f):
        def wrapper(self, *args):
            if self.api_client is None:
                raise DbNeedsLoginException()

            return f(self, *args)

        wrapper.__doc__ = f.__doc__
        return wrapper
    return decorate

class DropboxAdapter(object):
    def __init__(self, app_key, app_secret, token_filepath):
        self.__app_key = app_key
        self.__app_secret = app_secret
        self.__current_path = ''
        self.__token_filepath = token_filepath

        self.api_client = None

        try:
            token = open(self.__token_filepath).read()
            self.api_client = DropboxClient(token)
        except IOError:
            pass

    def need_auth(self):
        return self.api_client is None

    @_secure()
    def do_ls(self):
        """list files in current remote directory"""
        resp = self.api_client.metadata(self.__current_path)

        if 'contents' not in resp:
# TODO: Verify that this doesn't just happen if there are no entries.
            raise Exception("No contents returned.")

# Returns something like:
#
#[{u'bytes': 4,
#  u'client_mtime': u'Wed, 24 Jul 2013 06:04:01 +0000',
#  u'icon': u'page_white',
#  u'is_dir': False,
#  u'mime_type': u'application/octet-stream',
#  u'modified': u'Wed, 24 Jul 2013 06:04:01 +0000',
#  u'path': u'/test',
#  u'rev': u'1128dc84c',
#  u'revision': 1,
#  u'root': u'dropbox',
#  u'size': u'4 bytes',
#  u'thumb_exists': False}]

        return resp['contents']
        
#            for f in resp['contents']:
#                name = path.basename(f['path'])
#                encoding = locale.getdefaultlocale()[1]
#                self.stdout.write(('%s\n' % name).encode(encoding))

    @_secure()
    def do_cd(self, path):
        """change current working directory"""
        if path == "..":
            current_path_parts = self.__current_path.split("/")[0:-1]
            self.__current_path = "/".join(current_path_parts)
        else:
            self.__current_path += "/" + path

    @_secure()
    def do_logout(self):
        """log out of the current Dropbox account"""
        self.api_client = None
        unlink(self.__token_filepath)
        self.__current_path = ''

    @_secure()
    def do_mkdir(self, path):
        """create a new directory"""
        self.api_client.file_create_folder(self.__current_path + "/" + path)

    @_secure()
    def do_rm(self, path):
        """delete a file or directory"""
        self.api_client.file_delete(self.__current_path + "/" + path)

    @_secure()
    def do_mv(self, from_path, to_path):
        """move/rename a file or directory"""
        self.api_client.file_move(self.__current_path + "/" + from_path,
                                  self.__current_path + "/" + to_path)

    @_secure()
    def do_share(self, path):
        print self.api_client.share(path)['url']

#    @_secure()
#    def do_account_info(self):
#        """display account information"""
#        f = self.api_client.account_info()
#        pprint.PrettyPrinter(indent=2).pprint(f)

    @_secure()
# TODO: Only for small files. Produce a generator for large files.
    def do_get(self, from_path, data_receiver_cb):
        """
        Copy file from Dropbox to local file and print out the metadata.

        Examples:
        Dropbox> get file.txt ~/dropbox-file.txt
        """

        file_path = self.__current_path + "/" + from_path
        f, metadata = self.api_client.get_file_and_metadata(file_path)

        # (metadata, data, done_flag)
        data_receiver_cb(metadata, f.read(), True)

    @_secure()
    def do_thumbnail(self, from_path, data_receiver_cb, size='large', format='JPEG'):
        """
        Copy an image file's thumbnail to a local file and print out the
        file's metadata.

        Examples:
        Dropbox> thumbnail file.txt ~/dropbox-file.txt medium PNG
        """

        f, metadata = self.api_client.thumbnail_and_metadata(
                self.__current_path + "/" + from_path, size, format)

        # (metadata, data, done_flag)
        data_receiver_cb(metadata, f.read(), True)

    @_secure()
    def do_put(self, data, to_path):
        """
        Copy local file to Dropbox

        Examples:
        Dropbox> put ~/test.txt dropbox-copy-test.txt
        """

        file_path = self.__current_path + "/" + to_path
# TODO: This can also receive a file-like object.
        self.api_client.put_file(file_path, data)

    @_secure()
    def do_search(self, string):
        """Search Dropbox for filenames containing the given string."""

        return self.api_client.search(self.__current_path, string)

    def auth_1_get_url(self):
        """log in to a Dropbox account"""
        flow = DropboxOAuth2FlowNoRedirect(self.__app_key, self.__app_secret)

        authorize_url = flow.start()
        return authorize_url

    def auth_2_process_code(self, code):
        flow = DropboxOAuth2FlowNoRedirect(self.__app_key, self.__app_secret)
        access_token, user_id = flow.finish(code)

        with open(self.__token_filepath, 'w') as f:
            f.write(access_token)

        self.api_client = DropboxClient(access_token)

#da = DropboxAdapter(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, '/tmp/dropbox.auth')
#
#if da.need_auth():
#    print("We need authorization. Please visit:\n\n%s" % (da.auth_1_get_url()))
#    exit(1)
#
#da.auth_2_process_code('I8lp90gGP-EAAAAAAAAAAXHpGmbRriYaOAGIjco5e4g')
#
#if da.need_auth():
#    print("Auth was not stored successfully.")
#    exit(2)
#
#def data_receiver_cb(metadata, data, done_flag):
#    print("Received (%d) data bytes." % 
#          (len(data)))
#
#    pprint(metadata)
#    print
#
#    print(data)
#
#da.do_put('qrs', '/test')
#
#result = da.do_ls()
#da.do_get(result[0]['path'], data_receiver_cb)
#
#pprint(result)


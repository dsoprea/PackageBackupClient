from os.path import islink, isdir, abspath
from os import lstat
from cStringIO import StringIO
from struct import pack, unpack

from pbclient.fs.general import walk_with_empty, FS_IDX_FILEPATH, \
                                FS_IDX_MTIME, FS_IDX_ISDIR, FS_IDX_ISLINK

_ROW_PACKED_FMT = '<d??'
_ROW_PACKED_LEN = 10


class ManifestIterator(object):
    def __init__(self, manifest):
        self.__manifest = manifest
        self.__length = len(self.__manifest)

        self.reset()
    
    def __repr__(self):
        return ('<MAN-IT [%s] POS=(%d) LEN=(%d)>' % 
                (self.__path, self.__i, self.__length))
    
    def reset(self):
        pivot = self.__manifest.index('\0')
        self.__path = self.__manifest[0:pivot]
        self.__i = pivot + 1
        self.__index = 0
    
    def iterate(self):
        """Iterate through a manifest. We return a 2-tuple of header 
        information and a generate for the actual entries.
        """
    
        while 1:
            try:
                j = self.__manifest.index('\0', self.__i)
            except ValueError:
                break

            file_path = self.__manifest[self.__i:j]
            
            packed = self.__manifest[j + 1:j + _ROW_PACKED_LEN + 1]

            (mtime, is_dir_int, is_link_int) = \
                unpack(_ROW_PACKED_FMT, packed)

            is_dir = bool(is_dir_int)
            is_link = bool(is_link_int)

            yield (file_path, mtime, is_dir, is_link)

            self.__i = j + 1 + _ROW_PACKED_LEN
            self.__index += 1

    @property
    def path(self):
        return self.__path    

    @property
    def index(self):
        return self.__index

    @property
    def state(self):
        return (self.__i, self.__index)

    @state.setter
    def state(self, state_tuple):
        (self.__i, self.__index) = state_tuple

def build_manifest(path, files):
    path = abspath(path)

    list_ = ((f[FS_IDX_FILEPATH] + '\0' + 
              pack(_ROW_PACKED_FMT, 
                   f[FS_IDX_MTIME], 
                   f[FS_IDX_ISDIR], 
                   f[FS_IDX_ISLINK]))
             for f
             in files)

    # Write header.
    s = StringIO()
    s.write(path)
    s.write('\0')

    # Write entries.
    s.write(''.join(list_))
    
    return s.getvalue()

def get_files_from_path(path):
    path = abspath(path)

    files = []
    for (is_dir, file_path) in walk_with_empty(path):
        stat = lstat(file_path)

        files.append((file_path, 
                      stat.st_mtime, 
                      isdir(file_path), 
                      islink(file_path)))

    return files

def get_manifest_from_path(path):
    files = get_files_from_path(path)
    return build_manifest(path, files)


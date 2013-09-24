from os import lstat, listdir
from os.path import isdir
from Queue import Queue

FS_IDX_FILEPATH = 0
FS_IDX_MTIME = 1
FS_IDX_ISDIR = 2
FS_IDX_ISLINK = 3

def walk_with_empty(path, add_full_path=True):
    if path[-1] == '/':
        path = path[0:-1]

    q = Queue()
    q.put('')
    
    while q.empty() is False:
        sub_path = q.get()
        entries = listdir('%s/%s' % (path, sub_path))

        for entry in entries:
            file_path = ('%s%s/%s' % (path, sub_path, entry))
            whole_relative_path = ('%s/%s' % (sub_path, entry))

            is_dir_ = isdir(file_path)
            if is_dir_:
                q.put(whole_relative_path)

            if add_full_path is True:
                yield (is_dir_, file_path)
            else:
                yield (is_dir_, whole_relative_path)



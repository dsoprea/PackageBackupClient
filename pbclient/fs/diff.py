from pbclient.fs.general import FS_IDX_FILEPATH, FS_IDX_MTIME, FS_IDX_ISDIR, \
                                FS_IDX_ISLINK

def compare(original_gen, updated_gen):
    original_gen.reset()
    updated_gen.reset()

    original = original_gen.iterate()
    updated = updated_gen.iterate()
    
    original_dict = {}
    original_set_files = set()
    original_set_complete = set()
    
    updated_dict = {}
    updated_set_files = set()
    updated_set_complete = set()

    for entry in original:
        file_path = entry[FS_IDX_FILEPATH]

        original_dict[file_path] = \
            (entry[FS_IDX_MTIME], entry[FS_IDX_ISDIR], entry[FS_IDX_ISLINK])

        # This key characterizes the file-path to the point of uniqueness.
        # If there were two members and these two members were equal, the files
        # they represent would have to be equal, too.
        member_complete = ('%s-%s-%s-%s' % 
                           (file_path, entry[FS_IDX_MTIME], 
                            entry[FS_IDX_ISDIR], entry[FS_IDX_ISLINK]))

        original_set_complete.add(member_complete)
        original_set_files.add(file_path)

    add = []
    update = []
    for entry in updated:
        file_path = entry[FS_IDX_FILEPATH]

        original_dict[file_path] = \
            (entry[FS_IDX_MTIME], entry[FS_IDX_ISDIR], entry[FS_IDX_ISLINK])

        member_complete = ('%s-%s-%s-%s' % 
                   (file_path, entry[FS_IDX_MTIME], entry[FS_IDX_ISDIR], \
                    entry[FS_IDX_ISLINK]))
        updated_set_complete.add(member_complete)
        updated_set_files.add(file_path)

        if member_complete not in original_set_complete:
            if file_path in original_set_files:
                update.append(file_path)
            else:
                add.append(file_path)

    remove = tuple(original_set_files - updated_set_files)
    return (add, update, remove)


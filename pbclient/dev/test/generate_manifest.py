#!/usr/bin/python

from sys import argv, path, exit
path.insert(0, '.')

from pbclient.fs.file_manifest import get_manifest_from_path

if len(argv) < 3:
    print("Please provide a path and an output file.")
    exit(1)

(path, manifest_filepath) = argv[1:3]

manifest_data = get_manifest_from_path(path)

with file(manifest_filepath, 'wb') as f:
    f.write(manifest_data)

print("Wrote (%d) bytes to manifest." % 
      (len(manifest_data)))


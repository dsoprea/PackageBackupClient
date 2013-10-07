#!/usr/bin/python

from sys import argv, path, exit
path.insert(0, '.')

from pbclient.fs.file_manifest import ManifestIterator
from pbclient.fs.diff import compare

if len(argv) < 3:
    print("Please provide two manifests to compare.")
    exit(1)

(original_filepath, updated_filepath) = argv[1:3]

with file(original_filepath, 'rb') as f:
    original_manifest = f.read()

print("Read (%d) bytes for ORIGINAL manifest: %s" % 
      (len(original_manifest), original_filepath))

with file(updated_filepath, 'rb') as f:
    updated_manifest = f.read()

print("Read (%d) bytes for UPDATED manifest: %s" % 
      (len(updated_manifest), updated_filepath))

try:
    it_original = ManifestIterator(original_manifest)
except:
    print("There was an error while processing the ORIGINAL manifest.")
    raise
else:
    print("Original: %s" % (it_original))

try:       
    it_updated = ManifestIterator(updated_manifest)
except:
    print("There was an error while processing the UPDATED manifest.")
    raise
else:
    print("Updated: %s" % (it_updated))

(add, update, remove) = compare(it_original, it_updated)

print("Add:\n%s\n" % (add,))
print("Update:\n%s\n" % (update,))
print("Remove:\n%s\n" % (remove,))


from os import environ, remove, makedirs
from os.path import exists, expandvars
from json import load, dump
from fcntl import lockf, LOCK_EX, LOCK_UN
from shutil import rmtree

from p_m.config import PREFS_PATH, PREFS_FILENAME, PREFS_PATH_ENVIRON, \
                       LOCK_FILEPATH

_prefs_path = environ.get(PREFS_PATH_ENVIRON, expandvars(PREFS_PATH))
_prefs_filepath = ('%s/%s' % (_prefs_path, PREFS_FILENAME))

_default_prefs = { 'version': 1,
                   'system_name': None,
                   'api_key': None,
                   'api_secret': None }

# The prefs that always have to be given at initialization.
_required_keys = ('system_name', 'api_key', 'api_secret')

_max_lengths = { 'system_name': 30,
                 'api_key': 100,
                 'api_secret': 100 }

def _validate_prefs(prefs):
    if prefs is None:
        raise Exception("Prefs not loaded.")
    
    elif not prefs.get('system_name') or \
         not prefs.get('api_key') or \
         not prefs.get('api_secret'):

        raise Exception("System name [%s], API key [%s], and/or API secret "
                        "[%s] are not complete." % 
                        (prefs.get('system_name'),
                         prefs.get('api_key'), 
                         prefs.get('api_secret')))


class Prefs(object):
    def __init__(self):
        self.__prefs = None

    def initialize(self, values):
        self.__prefs = _default_prefs

        possible = set(self.__prefs.keys())
        required = set(_required_keys)
        given = set(values.keys())

        # Check if 'given' is completely within 'possible'.
        if given.issubset(possible) is False:
            raise Exception("One or more given prefs were invalid: %s" % 
                            ((given - possible),))

        # Check if 'required' is completely within 'given'.
        if required.issubset(given) is False:
            raise Exception("One or more required prefs were omitted: %s" % 
                            ((required - given),))

        for k, v in values.iteritems():
            self.set(k, v)

    def set(self, key, value):
        if key not in self.__prefs:
            raise KeyError('Can not set invalid key [%s].' % (key))
        elif len(value) > _max_lengths[key]:
            raise Exception("Value [%s] for key [%s] exceeds maximum length of"
                            " (%d)." % (_max_lengths[key]))

        self.__prefs[key] = value

    def get(self, key):
        return self.__prefs[key]

    def get_dict(self):
        self.load()
        return self.__prefs

    def load(self):
        if self.__prefs is not None:
            return

        with file(_prefs_filepath) as f:
            self.__prefs = load(f)
        
    def exists(self):
        return exists(_prefs_filepath)
    
    def clear(self):
        self.__prefs = None
        rmtree(_prefs_path)
    
    def save(self):
        _validate_prefs(self.__prefs)

        if exists(_prefs_path) is False:
            makedirs(_prefs_path)

        with file(LOCK_FILEPATH, 'w') as l:
            lockf(l, LOCK_EX)        

            with file(_prefs_filepath, 'w') as f:
                dump(self.__prefs, f)

            lockf(l, LOCK_UN)


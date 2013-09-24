import json

from os import environ, remove, makedirs
from os.path import exists, expandvars
from fcntl import lockf, LOCK_EX, LOCK_UN
from shutil import rmtree

from pmclient.config import PREFS_PATH, PREFS_FILENAME, PREFS_PATH_ENVIRON, \
                            LOCK_FILEPATH, BACKUP_AGENT_MODULE_PREFIX

_prefs_path = environ.get(PREFS_PATH_ENVIRON, expandvars(PREFS_PATH))
_prefs_filepath = ('%s/%s' % (_prefs_path, PREFS_FILENAME))

_default_prefs = { 'version': 1,
                   'system_name': None,
                   'api_key': None,
                   'api_secret': None,
                   'backup_agent_class': 'sftp_backup_client.SftpBackupClient',
                   'backup_agent_json_file': None }

# The prefs that always have to be given at initialization.
_required_keys = ('system_name', 'api_key', 'api_secret')

_max_lengths = { 'system_name': 30,
                 'api_key': 100,
                 'api_secret': 100,
                 'backup_agent_class': 200,
                 'backup_agent_json_file': 256 }

def _get_backup_agent(backup_class_name):
    fq_class_name = ('%s%s' % (BACKUP_AGENT_MODULE_PREFIX, backup_class_name))
    period_at = fq_class_name.rfind('.')
    module_name = fq_class_name[:period_at]
    class_name = fq_class_name[period_at + 1:]

    module = __import__(module_name, fromlist=[class_name])

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError("Could not find/import class [%s] from [%s]." % 
                          (class_name, module_name))

def _validate_prefs(prefs):
    if prefs is None:
        raise Exception("Prefs not loaded.")
    
    elif prefs.get('system_name') == '' or \
         prefs.get('api_key') == '' or \
         prefs.get('api_secret') == '':

        raise Exception("System name [%s], API key [%s], and/or API secret "
                        "[%s] are not complete." % 
                        (prefs.get('system_name'),
                         prefs.get('api_key'), 
                         prefs.get('api_secret')))

    backup_agent_class_name = prefs.get('backup_agent_class').strip()
    if backup_agent_class_name != '':
        _get_backup_agent(backup_agent_class_name)

    backup_agent_json_file = prefs.get('backup_agent_json_file').strip()
    if backup_agent_json_file != '':
        with open(backup_agent_json_file) as f:
            json.load(f)

    if (backup_agent_class_name == '') ^ (backup_agent_json_file == ''):
        raise Exception("Both 'backup_agent_class' and "
                        "'backup_agent_json_file' must either be given or "
                        "omitted.")

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

        for k, v in values.items():
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

        with open(_prefs_filepath) as f:
            self.__prefs = json.load(f)
        
    def exists(self):
        return exists(_prefs_filepath)
    
    def clear(self):
        self.__prefs = None
        rmtree(_prefs_path)
    
    def save(self):
        _validate_prefs(self.__prefs)

        if exists(_prefs_path) is False:
            makedirs(_prefs_path)

        with open(LOCK_FILEPATH, 'w') as l:
            lockf(l, LOCK_EX)        

            with open(_prefs_filepath, 'w') as f:
                json.dump(self.__prefs, f)

            lockf(l, LOCK_UN)


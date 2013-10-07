import json

from os import environ, remove, makedirs, utime
from os.path import exists, join
from fcntl import lockf, LOCK_EX, LOCK_UN
from shutil import rmtree
from collections import OrderedDict

from pbclient.config import PREFS_PATH, PREFS_FILENAME, LOCK_FILEPATH, \
                            BACKUP_AGENT_MODULE_PREFIX, \
                            DEFAULT_BACKUP_MODULE, BACKUP_CONFIG_FILENAME
from pbclient.libs.random_utility.text_prompts import text_prompts

_prefs_path = PREFS_PATH
_prefs_filepath = ('%s/%s' % (_prefs_path, PREFS_FILENAME))

_default_prefs = { 'version': 1,
                   'system_name': '',
                   'api_key': '',
                   'api_secret': '',
                   'backup_agent_class': DEFAULT_BACKUP_MODULE }

_prompt_info = OrderedDict([('system_name', ('System Name', True, False)),
                           ('api_key', ('API Key', True, True)),
                           ('api_secret', ('API Secret', True, True))])

# The prefs that always have to be given at initialization.
_required_keys = ('system_name', 'api_key', 'api_secret')

_max_lengths = { 'system_name': 30,
                 'api_key': 100,
                 'api_secret': 100,
                 'backup_agent_class': 200 }

def _get_backup_config():
    """Recover the backup config."""

    backup_config_filepath = join(PREFS_PATH, BACKUP_CONFIG_FILENAME)

    try:
        with open(backup_config_filepath) as f:
            config_str = f.read()
    except IOError:
        with open(backup_config_filepath, 'w+') as f:
            pass

        config_str = ''

    locals_ = {}
    exec(config_str, {}, locals_)

    return locals_

def _get_backup_agent(backup_class_name):
    fq_class_name = ('%s%s' % (BACKUP_AGENT_MODULE_PREFIX, backup_class_name))
    period_at = fq_class_name.rfind('.')
    module_name = fq_class_name[:period_at]
    class_name = fq_class_name[period_at + 1:]

    module = __import__(module_name, fromlist=[class_name])

    try:
        cls = getattr(module, class_name)
    except AttributeError:
        raise ImportError("Could not find/import class [%s] from [%s]." % 
                          (class_name, module_name))

    locals_ = _get_backup_config()

    # Create the instance.
# TODO: Implement this.
    return None#cls(**locals_)

def _validate_prefs(prefs_dict):
    if prefs_dict['system_name'] == '' or \
         prefs_dict['api_key'] == '' or \
         prefs_dict['api_secret'] == '':

        raise Exception("System name [%s], API key [%s], and/or API secret "
                        "[%s] are not complete." % 
                        (prefs_dict['system_name'],
                         prefs_dict['api_key'], 
                         prefs_dict['api_secret']))

    backup_agent_class_name = prefs_dict['backup_agent_class'].strip()
    if backup_agent_class_name != '':
        _get_backup_agent(backup_agent_class_name)

class Prefs(object):
    def __init__(self):
        self.__prefs = None
        if exists(_prefs_path) is False:
            makedirs(_prefs_path)

#    def initialize(self, values):
#        self.__prefs = _default_prefs
#
#        possible = set(self.__prefs.keys())
#        required = set(_required_keys)
#        given = set(values.keys())
#
#        # Check if 'given' is completely within 'possible'.
#        if given.issubset(possible) is False:
#            raise Exception("One or more given prefs were invalid: %s" % 
#                            ((given - possible),))
#
#        # Check if 'required' is completely within 'given'.
#        if required.issubset(given) is False:
#            raise Exception("One or more required prefs were omitted: %s" % 
#                            ((required - given),))
#
#        for k, v in values.items():
#            self.set(k, v)
#
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

        with open(LOCK_FILEPATH, 'w') as l:
            lockf(l, LOCK_EX)        

            with open(_prefs_filepath, 'w') as f:
                json.dump(self.__prefs, f)

            lockf(l, LOCK_UN)

    def load_from_console(self):

        exists = self.exists()
        if exists is True:
            self.load()

        def get_default(id_):
            return self.__prefs[id_] if exists else _default_prefs[id_]

        prompts = OrderedDict([ (id_, 
                                 (label_text, 
                                  is_required, 
                                  get_default(id_),
                                  False,
                                  can_truncate)) 
                              for (id_, (label_text, is_required, can_truncate)) 
                              in _prompt_info.items() ])

        responses = text_prompts(prompts)
        
        for k, v in _default_prefs.items():
            if k not in responses:
                responses[k] = v
        
        self.__prefs = responses
        self.save()


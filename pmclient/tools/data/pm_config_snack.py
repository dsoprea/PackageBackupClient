from os.path import expanduser, exists

from snackwich.exceptions import GotoPanelException, QuitException
from pmclient.prefs import Prefs

_default_system_name = '(set a friendly name, here)'

values = { 'system_name': _default_system_name,
           'api_key': '',
           'api_secret': '',
           #'backup_agent_class': 'sftp_backup_client.SftpBackupClient',
           #'backup_agent_json_file': '~/sftp_backup_client.json' 
           }

prefs = Prefs()
if prefs.exists():
    values = prefs.get_dict()

BTN_OK = 'ok'
BTN_CANCEL = 'cancel'

def post_callback(sw, key, result, expression, screen):
#    global values

    if result['button'] == BTN_CANCEL or result['is_esc']:
        raise QuitException()

#    values = dict(zip(('system_name', 'api_key', 'api_secret', \
#                       'backup_agent_class', 'backup_agent_json_file'), 
#                      result['values']))

    values_in = dict(zip(('system_name', 'api_key', 'api_secret'), 
                          result['values']))

    for k, v in values_in.items():
        values_in[k] = v.strip()

    values.update(values_in)

    if values['system_name'] == '' or values['api_key'] == '' or \
       values['api_secret'] == '':
        raise GotoPanelException('validation_error')

# TODO: Test this.
    elif values['system_name'] == _default_system_name:
        raise GotoPanelException('validation_error_system_name')

# TODO: Validate the backup-agent class, here, rather than later when all we
#       can do is terminate.

#    values['backup_agent_json_file'] = \
#        expanduser(values['backup_agent_json_file'])

# TODO: Only implement this once we provide the functionality.
#    if exists(values['backup_agent_json_file']) is False:
#        raise GotoPanelException('validation_error_agent_json')


# Required in order to Snackwich to find the actual configuration.
config = [{ '_name': 'window1',
            '_widget': 'entry',
            'title': 'Client Information',
            'text': 'Please enter your client information.',
            'prompts': [('System Name', values['system_name']),
                        ('API Key', values['api_key']),
                        ('API Secret', values['api_secret']),
#                        ('Backup Class', values['backup_agent_class']),
#                        ('Backup Config', values['backup_agent_json_file'])
],
            'width': 100,
            'entryWidth': 80,
            '_post_cb': post_callback },

          { '_name': 'validation_error',
            '_widget': 'choice',
            '_next': 'window1',
            'title': 'Error',
            'text': "Please set all fields.",
            'buttons': ['OK'],
           },

          { '_name': 'validation_error_system_name',
            '_widget': 'choice',
            '_next': 'window1',
            'title': 'Error',
            'text': "Please set the system name to be something unique to this system.",
            'buttons': ['OK'],
           },

          { '_name': 'validation_error_agent_json',
            '_widget': 'choice',
            '_next': 'window1',
            'title': 'Error',
            'text': "The backup-client JSON file does not exist.",
            'buttons': ['OK'],
           },
           ]


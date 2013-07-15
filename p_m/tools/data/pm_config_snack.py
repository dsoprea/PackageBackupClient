from snackwich.exceptions import GotoPanelException, QuitException

from p_m.prefs import Prefs
values = { 'system_name': '',
           'api_key': '',
           'api_secret': '' }

prefs = Prefs()
if prefs.exists():
    values = prefs.get_dict()

BTN_OK = 'ok'
BTN_CANCEL = 'cancel'

def post_callback(sw, key, result, expression, screen):
    global values

    if result['button'] == BTN_CANCEL or result['is_esc']:
        raise QuitException()

    values = dict(zip(('system_name', 'api_key', 'api_secret'), 
                      result['values']))

    for k, v in values.items():
        values[k] = v.strip()

    if values['system_name'] == '' or values['api_key'] == '' or \
       values['api_secret'] == '':
        raise GotoPanelException('validation_error')

# Required in order to Snackwich to find the actual configuration.
config = [{ '_name': 'window1',
            '_widget': 'entry',
            'title': 'Client Information',
            'text': 'Please enter your client information.',
            'prompts': [('System Name', values['system_name']),
                        ('API Key', values['api_key']),
                        ('API Secret', values['api_secret'])],
            'width': 100,
            'entryWidth': 80,
            '_post_cb': post_callback },

          { '_name': 'validation_error',
            '_widget': 'choice',
            '_next': 'window1',
            'title': 'Error',
            'text': "Please fill all fields.",
            'buttons': ['OK'],
           }]


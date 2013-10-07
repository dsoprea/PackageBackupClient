from os import environ
from os.path import expandvars

CLIENT_ID = 'e9d891152bb45b453111fbc4bda67f82c180450ebf50cc2ca265e96b82b149f1'\
            '00e06'
PREFS_PATH = environ.get('PB_PREFS_PATH', 
                         expandvars('$HOME/.package_backup'))
PREFS_FILENAME = 'prefs.json'
LOCK_FILEPATH = '/tmp/pm_prefs.lock'

API_CLIENT_ID_HEADER = 'X-Api-Client-Id'
API_AUTH_KEY_HEADER = 'X-Api-Auth-Key'
API_AUTH_SECRET_HEADER = 'X-Api-Auth-Secret'

API_DEFAULT_URL_PREFIX = 'https://www.packagebackup.com'
API_URL_PREFIX = environ.get('PB_API_URL_PREFIX', 
                             API_DEFAULT_URL_PREFIX)

API_URL_LIST_PUSH = ('%s%s' % (API_URL_PREFIX, '/api/list/push'))
API_URL_LIST_GET = ('%s%s' % (API_URL_PREFIX, '/api/list/get'))

def api_is_success(status_code):
    return (status_code == 200)

BACKUP_AGENT_MODULE_PREFIX = 'pbclient.backup.'
DEFAULT_BACKUP_MODULE = 'sftp_backup_client.SftpBackupClient'
BACKUP_CONFIG_FILENAME = 'backup.py'


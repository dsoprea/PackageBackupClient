from requests import post
from bz2 import compress

from p_m.config import CLIENT_ID, API_URL_LIST_PUSH, API_CLIENT_ID_HEADER, \
                       API_AUTH_KEY_HEADER, API_AUTH_SECRET_HEADER

from p_m.prefs import Prefs


class Client(object):
    def __init__(self):
        self.__prefs = Prefs()
        self.__prefs.load()

    def __send(self, type_phrase, url, data_extra):
        data = { 'client_version': self.__prefs.get('version'),
                 'system_name': self.__prefs.get('system_name') }

        data.update(data_extra)

        headers = { API_CLIENT_ID_HEADER: CLIENT_ID,
                    API_AUTH_KEY_HEADER: self.__prefs.get('api_key'),
                    API_AUTH_SECRET_HEADER: self.__prefs.get('api_secret') }

        r = post(url, headers=headers, data=data, verify=True)
        if api_is_success(r.status) is False:
            raise Exception("API connection failed with (%d) for [%s]." % 
                            (r.status, type_phrase))
        
        response = r.json()
        if response.success is False:
            raise Exception("Request returned failure for [%s]: %s" % 
                            (type_phrase, response))

        return response

    def list_push(self, system_info, package_list_raw):
        package_list_bz2 = compress(package_list_raw)

        with file('/tmp/packages.bz2', 'w') as f:
            f.write(package_list_bz2)

        data = { 'repo_type': system_info.repo_type,
                 'os_type': system_info.os_type, 
                 'os_version': system_info.os_version, 
                 'data': package_list_bz2 }

        self.__send('list_push', API_URL_LIST_PUSH, data)


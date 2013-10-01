import logging
import time

from requests import post
from bz2 import compress
from base64 import b64encode
from time import tzname

from pmclient.config import CLIENT_ID, API_URL_LIST_PUSH, \
                            API_CLIENT_ID_HEADER, API_AUTH_KEY_HEADER, \
                            API_AUTH_SECRET_HEADER, api_is_success

from pmclient.prefs import Prefs


class Client(object):
    def __init__(self):
        self.__prefs = Prefs()
        self.__prefs.load()

    def __send(self, type_phrase, url, data_extra):
        logging.debug("Sending to [%s]." % (url))

        data = { 'cv': self.__prefs.get('version'),
                 'sn': self.__prefs.get('system_name') }

        data.update(data_extra)

        headers = { API_CLIENT_ID_HEADER: CLIENT_ID,
                    API_AUTH_KEY_HEADER: self.__prefs.get('api_key'),
                    API_AUTH_SECRET_HEADER: self.__prefs.get('api_secret') }

        r = post(url, headers=headers, data=data, verify=True)
        is_decoded = False

        try:
            response = r.json()
        except:
            response = r.content
            
            if not response:
                response = '<no content>'
        else:
            is_decoded = True

# TODO: Replace Exception() with specific exceptions.
        if api_is_success(r.status_code) is False:
            reason = response['message'] if is_decoded is True else r.reason
            raise Exception("API connection failed with (%d) for [%s].\n\n%s" % 
                            (r.status_code, type_phrase, reason))
        elif is_decoded is False:
            raise Exception("Could not decode response as JSON:\n%s" % 
                            (response))
        elif response['error'] is not None:
            raise Exception("Request returned failure for [%s] (%s).\n\n%s" % 
                            (type_phrase, response['error'], 
                             response['message']))

        return response['result']

    def list_push(self, system_info, package_list_raw):
        logging.debug("Pushing list to system [%s]." % (system_info))
    
        package_list_bz2 = compress(package_list_raw)

        data = { 'rt': system_info.repo_type,
                 'ot': system_info.os_type, 
                 'ov': system_info.os_version, 
                 'd': b64encode(package_list_bz2),
                 'tn': tzname[0] }

        return self.__send('list_push', API_URL_LIST_PUSH, data)


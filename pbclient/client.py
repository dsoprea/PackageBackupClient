import logging
import time
import json

from requests import post
from bz2 import compress
from base64 import b64encode
from time import tzname
from datetime import datetime

from pbclient.constants.time import DATE_FORMAT, DATE_FORMAT_HUMAN
from pbclient.config import CLIENT_ID, API_URL_LIST_PUSH, API_URL_LIST_GET, \
                            API_CLIENT_ID_HEADER, API_AUTH_KEY_HEADER, \
                            API_AUTH_SECRET_HEADER, api_is_success
from pbclient.exceptions.http import HttpRequestError
from pbclient.prefs import Prefs
from pbclient.utility import stringify


class Client(object):
    def __init__(self, system_profiler_cls):
        self.__prefs = Prefs()
        self.__prefs.load()

        self.__system_profiler = system_profiler_cls()
        self.__system_info = self.__system_profiler.get_system_info()

    def __send(self, type_phrase, url, data_extra, is_raw=False):
        logging.debug("Sending to [%s]." % (url))

        packaged_system_info =  { 'sn': self.__prefs.get('system_name'),
                                  'rt': self.__system_info.repo_type,
                                  'ot': self.__system_info.os_type, 
                                  'ov': self.__system_info.os_version, 
                                  'tn': tzname[0] }

        packaged_system_info_encoded = json.dumps(packaged_system_info)

        data = { 'cv': self.__prefs.get('version'),

                 # System info.
                 'si': packaged_system_info_encoded }

        data.update(data_extra)

        headers = { API_CLIENT_ID_HEADER: CLIENT_ID,
                    API_AUTH_KEY_HEADER: self.__prefs.get('api_key'),
                    API_AUTH_SECRET_HEADER: self.__prefs.get('api_secret') }

        r = post(url, headers=headers, data=data, verify=True)
        self.__response_context = r

        if is_raw is True:
            if api_is_success(r.status_code) is False:
                raise HttpRequestError(r, "API connection failed for request "
                                          "[%s]." % (type_phrase))

            response_data = r.content
        else:
            is_decoded = False

            try:
                response = r.json()
            except:
                response = r.content
                
                if not response:
                    response = '<no content>'
            else:
                is_decoded = True

            if api_is_success(r.status_code) is False:
                message = response['message'] if is_decoded is True \
                                              else '<could not decode>'

                raise HttpRequestError(r, "API connection failed for request "
                                          "[%s]: %s" % (type_phrase, message))
            elif is_decoded is False:
                raise Exception("Could not decode response:\n%s" % (response))
            elif response['error'] is not None:
                raise Exception("Request returned failure for [%s] (%s).\n\n%s" % 
                                (type_phrase, response['error'], 
                                 response['message']))

            response_data = response['result']

        return response_data

    def list_push(self, package_list_raw):
        logging.debug("Pushing list to system [%s]." % (self.__system_info))
    
        package_list_bz2 = compress(package_list_raw)

        data = { 'd': b64encode(package_list_bz2) }

        list_data = self.__send('list_push', API_URL_LIST_PUSH, data)
        return stringify(list_data)

    def list_get(self, list_name=None, date_string=None):
        """Retrieve a list. If no name is provided, the most recent will be 
        retrieved.
        """

        logging.debug("Recalling list for system [%s]." % (self.__system_info))

        if date_string is not None:
            try:
                datetime.strptime(date_string, DATE_FORMAT)
            except ValueError as e:
                raise ValueError("Date string does not look like %s: %s" % 
                                 (DATE_FORMAT_HUMAN, str(e)))

        if list_name is None:
            list_name = ''
        
        if date_string is None:
            date_string = ''

        data = { 'n': list_name,
                 'd': date_string }

        list_data_bytes = self.__send('list_get', 
                                      API_URL_LIST_GET, 
                                      data, 
                                      is_raw=True)

        list_data = stringify(list_data_bytes)
        list_name = stringify(self.__response_context.headers['x-listname'])
        list_filename = stringify(self.__response_context.headers['x-listfilename'])
        
        return (list_name, list_filename, list_data)


import logging

from argparse import ArgumentParser
from sys import stderr, stdout

from pbclient.constants.http import INTERNAL_HTTP_NOT_FOUND
from pbclient.exceptions.http import HttpRequestError
from pbclient.client import Client

def render_list_info(system_profiler):
    parser = ArgumentParser(description='Retrieve package-list for DPKG.')

    parser.add_argument('outputfile', 
                        help="File to write to ('-' for standard output)")

    parser.add_argument('-v', '--verbose', 
                        action='store_true', 
                        help="Show logging.")

    parser.add_argument('-n', '--name', help="List name")
    parser.add_argument('-d', '--date', help="List date")

    result = parser.parse_args()

    if result.verbose:
        from pbclient import logging_config

    try:
        list_info = Client(system_profiler).list_get(list_name=result.name, 
                                                     date_string=result.date)
    except HttpRequestError as e:
        if e.code == INTERNAL_HTTP_NOT_FOUND:
            stderr.write("No list found.\n\n")
            exit(2)

        raise

    (list_name, list_filename, content) = list_info

    stderr.write("Writing list with name [%s] to [%s]. Please note that, if "
                 "this name resembles a timestamp, it will be in the UTC "
                 "timezone.\n\n" % (list_name, result.outputfile))

    if result.outputfile == '-':
        stdout.write(content)
    else:
        with open(result.outputfile, 'w+') as f:
            f.write(content)


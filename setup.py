#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.install import install

from pbclient.install_phases import pre_install, post_install, REPO_TYPE, \
                                    REPO_DPKG, REPO_PACMAN

version = '0.6.4'

_scripts = ['pbclient/tools/pb_config']

if REPO_TYPE == REPO_DPKG:
    _scripts.append('pbclient/tools/pb_pushlist_dpkg')
    _scripts.append('pbclient/tools/pb_getlist_dpkg')
else:
    _scripts.append('pbclient/tools/pb_pushlist_pacman')
    _scripts.append('pbclient/tools/pb_getlist_pacman')


class custom_install(install):
    def run(self):
        pre_install()
        install.run(self)
        post_install()

setup(name='pbclient',
      version=version,
      description="A client for the http://packagebackup.com package-list backup service.",
      long_description="A client for the Package Backup package-list backup service.",
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Environment :: Console',
                   'Programming Language :: Python :: 3.0'
                  ],
      keywords='package-list packagelist backup packagebackup package-backup',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/pbclient',
      license='GPL2',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
        'pysecure',
        'python-crontab',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      cmdclass={'install': custom_install
               },
      scripts=_scripts
      )


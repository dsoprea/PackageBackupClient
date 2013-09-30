#!/usr/bin/python

from setuptools import setup, find_packages

version = '0.1.1'

setup(name='pmclient',
      version=version,
      description="A client for the Package Backup package-list backup service.",
      long_description="A client for the Package Backup package-list backup service.",
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Environment :: Console',
                   'Programming Language :: Python :: 3.0'
                  ],
      keywords='package-list packagelist backup packagebackup package-backup',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/PmClient',
      license='GPL2',
      packages=['pmclient'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'requests',
        'snackwich',
        'pysecure'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )


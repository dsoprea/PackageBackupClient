Requirements
============

requests
pysecure


Installation
============

This client is meant to be used with an account on Package 
Backup. Following the directions there, you will:

1) Download the PM client (this).
2) Configure the PM client for either DPKG or PACMAN
3) Schedule it in Cron.

Once all steps are completed, daily backups will be automatically captured and 
available for you, for at least two months.

For more information, please visit http://www.packagebackup.com .


Removing
========

To remove the client, do the following:

> Remove the "pbclient" entry from the system crontab (root).
> Delete the symlinked "pb" tools:
  > pb_config
  > pb_pushlist_dpkg
  > pb_pushlist_pacman
  > pb_getlist_dpkg
  > pb_getlist_pacman

> Run "pip uninstall pbclient"


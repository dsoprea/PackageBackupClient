from subprocess import Popen, PIPE
from os import environ, unlink
from sys import version_info

REPO_DPKG = 'dpkg'
REPO_PACMAN = 'pacman'

REPO_TYPES = set([REPO_DPKG, REPO_PACMAN])

def _determine_repo_type():
    """Return the name of the system's package repository."""

    prescribed = environ.get('REPO_TYPE')
    if prescribed is not None:
        if prescribed not in REPO_TYPES:
            raise ValueError("Prescribed repo-type [%s] is not valid." % 
                             (prescribed))
        
        return prescribed

    repo = []

    try:
        Popen('dpkg', stdout=PIPE, stderr=PIPE)
    except FileNotFoundError:
        pass
    else:
        repo.append(REPO_DPKG)

    try:
        Popen('pacman', stdout=PIPE, stderr=PIPE)
    except:
        pass
    else:
        repo.append(REPO_PACMAN)

    len_ = len(repo)

    if len_ == 0:
        raise SystemError("Could not identify a repository type.")
    elif len_ > 1:
        raise SystemError("All checked repository tools were found. We don't "
                          "know which to elect.")

    return repo[0]

REPO_TYPE = _determine_repo_type()

if REPO_TYPE == REPO_DPKG:
    _TOOL_PUSHLIST_FILENAME = "pb_pushlist_dpkg"
else:
    _TOOL_PUSHLIST_FILENAME = "pb_pushlist_pacman"

def _get_full_filepath(executable):
    p = Popen(['which', executable], stdout=PIPE, stderr=PIPE)
    (stdout_data, ignore_) = p.communicate()
    file_path = stdout_data.strip().decode('ASCII')

    if file_path == '':
        raise LookupError("Could not resolve executable: %s" % (executable))

    return file_path

class _CrontabConfig(object):
    __comment = "Package Backup push tool"

    def __init__(self):
        from crontab import CronTab    
        self.__cron = CronTab()

    def __get_existing(self):
        list_ = self.__cron.find_comment(self.__class__.__comment)
        if len(list_) == 0:
            raise LookupError()

        return list_[0]

    def clear_existing(self):
        try:
            job = self.__get_existing()
        except LookupError:
            pass
        else:
            print("Removing existing crontab job: %s" % (self.__comment))

            self.__cron.remove(job)
            self.__cron.write()

    def install(self):
        self.clear_existing()

        pushtool_filepath = _get_full_filepath(_TOOL_PUSHLIST_FILENAME)
        print("Installing tool [%s] as crontab job [%s]." % 
              (pushtool_filepath, self.__comment))

        job = self.__cron.new(command=pushtool_filepath)
        job.meta(self.__class__.__comment)
        job.special = "@daily"
        
        self.__cron.write()

_crontab_config = _CrontabConfig()

def pre_install():
    if version_info[0] < 3:
        raise SystemError("Please install using Python 3.x .")

    try:
        Popen('lsb_release', stdout=PIPE, stderr=PIPE)
    except FileNotFoundError:
        print("lsb_release doesn't seem to be available. Please make sure "
              "that it's installed.")
        raise

    # The setuptools requirements check should catch this, but an exception
    # about a missing shared library might be confusing.
    print("Verifying that PySecure exists.")

    try:
        import pysecure
    except:
        print("PySecure can not be loaded. Please make sure that it's "
              "installed, along with its dependencies.")
        raise

def post_install():
# Is not visible when invoked from within Setuptools.
#    print("")
#    print("Starting config.")
#
#    from pbclient.prefs import Prefs
#    Prefs().load_from_console()
#
    print("Installing crontab job.")
    _crontab_config.install()


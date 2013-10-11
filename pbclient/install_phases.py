from subprocess import Popen, PIPE
from os import environ, unlink
from sys import version_info

_REPO_DPKG = 'dpkg'
_REPO_PACMAN = 'pacman'

_REPO_TYPES = set([_REPO_DPKG, _REPO_PACMAN])

_TOOL_PUSHLIST_DPKG = "pb_pushlist_dpkg"
_TOOL_PUSHLIST_PACMAN = "pb_pushlist_pacman"

_CRON_PUSH_TOOL_MAP = { _REPO_DPKG: _TOOL_PUSHLIST_DPKG,
                        _REPO_PACMAN: _TOOL_PUSHLIST_PACMAN }

def _get_full_filepath(executable):
    p = Popen(['which', executable], stdout=PIPE, stderr=PIPE)
    (stdout_data, ignore_) = p.communicate()
    file_path = stdout_data.strip().decode('ASCII')

    if file_path == '':
        raise LookupError("Could not resolve executable: %s" % (executable))

    return file_path

def _determine_repo_type():
    """Return the name of the system's package repository."""

    prescribed = environ.get('REPO_TYPE')
    if prescribed is not None:
        if prescribed not in _REPO_TYPES:
            raise ValueError("Prescribed repo-type [%s] is not valid." % 
                             (prescribed))
        
        return prescribed

    repo = []

    try:
        Popen('dpkg', stdout=PIPE, stderr=PIPE)
    except FileNotFoundError:
        pass
    else:
        repo.append(_REPO_DPKG)

    try:
        Popen('pacman', stdout=PIPE, stderr=PIPE)
    except:
        pass
    else:
        repo.append(_REPO_PACMAN)

    len_ = len(repo)

    if len_ == 0:
        raise SystemError("Could not identify a repository type.")
    elif len_ > 1:
        raise SystemError("All checked repository tools were found. We don't "
                          "know which to elect.")

    return repo[0]


class _CrontabConfig(object):
    __comment = "Package Backup push tool"

    def __init__(self):
        from crontab import CronTab    
        self.__cron = CronTab()

    def __get_pushtool_filepath(self):
        repo_type = _determine_repo_type()
        tool_name = _CRON_PUSH_TOOL_MAP[repo_type]
        return _get_full_filepath(tool_name)

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

        pushtool_filepath = self.__get_pushtool_filepath()
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
    print("")
    print("Starting config.")

    from pbclient.prefs import Prefs
    Prefs().load_from_console()

    print("Installing crontab job.")
    _crontab_config.install()


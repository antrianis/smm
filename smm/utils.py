import os
import errno
import shutil
import json
import csv
from distutils.util import strtobool
from logging import getLogger, basicConfig


def configure_logger(logging_level):
    basicConfig(
        format='%(asctime)-8s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        level=logging_level
    )

logger = getLogger(__name__)


def user_yes_no_query(question):
    while True:
        print '%s (y/[n])' % question,
        try:
            inp = raw_input()
            return strtobool(inp.lower())
        except ValueError:
            if not inp:
                return False
            continue


def len_cap(s, l):
    if s and l >= 3:
        return s if len(s) <= l else s[:l - 3] + "..."
    else:
        return ""


def get_parts_delimeter_quoted(input_line, delimiter='/'):
    """
        Given a str
        it returns a list of the str tokens
        split on / except for / in quotes.
    """
    reader = csv.reader([input_line], delimiter=delimiter)
    return next(reader)


def get_env(env_name, def_value=None):
    """Return OS env variable value if env_name exists,
    otherwise return default value

    :param str env_name: Environment variable
    :param str def_value: Default value
    :return: OS env value if present, otherwise def_value
    :rtype: str
    """
    ret_val = os.environ.get(env_name, def_value)
    # make sure that environment variable is non space
    return ret_val if ret_val.strip() else def_value


def get_abs_path(path):
    """Return OS absolute path for the given path

    :param str path: OS path
    :return: OS absolute path
    :rtype: str
    """
    return os.path.normpath(path) if os.path.isabs(path) else os.path.normpath(
        os.path.abspath(
            os.path.expanduser(path)))


def is_file(path):
    """Return True if file exits, False otherwise

    :param str path: OS path
    :return: True if file exists, False otherwise
    :rtype: bool
    """
    return os.path.isfile(path)


def check_configuration(db_path):
    """Return True if db_path folder exists and
    it has sufficient write access rights

    :param str db_path: OS path
    :return: True if db_path location exists and it's writable
    :rtype: bool
    """
    full_db_path = get_abs_path(db_path)
    # if folder exists
    if os.path.isdir(full_db_path):
        if os.access(full_db_path, os.W_OK | os.X_OK):
            return True
    return False


def init_smmdbstore(db_path, init_state):
    """Write initial state to the file on the db_path

    :param str db_path: OS file path
    """
    with open(db_path, 'w') as outfile:
        json.dump(init_state, outfile)


def create_db_path(db_path):
    """Create db_path hierarchy

    :param str db_path: OS folder path
    """
    full_db_path = get_abs_path(db_path)
    try:
        os.makedirs(full_db_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def copy_file(file_path, new_file_path):
    """Copy file from file_path to new_file_path

    :param str file_path: File location
    :param new_file_path: Target location
    :return:
    """
    shutil.copy2(file_path, new_file_path)


def get_file_name(db_path, file_name):
    """Return concatenated abs file path

    :param str db_path: Folder path
    :param str file_name: File name
    :return: Full file path
    :rtype: str
    """
    return get_abs_path(os.path.join(db_path, file_name))

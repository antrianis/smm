import string
from smm.utils import get_env, get_abs_path

# Templates
tmpl_missing_key = string.Template('Missing key [$key].')

DB_FILE_NAME = 'smmdbstore.json'
DB_DEF_PATH = '~/.smmdbstore/'
DB_FILE_NAME_BKP = '.' + DB_FILE_NAME + '.backup'
GROUP_ID = '__groups__'
DATA_ID = '__data__'
COUNT_ID = '__count__'
OWNER_ID = '__owner__'
COMM_TEXT = 'text'
COMM_GROUP = 'group'
COMM_DESC = 'description'
DB_PATH = get_env('SMMENVDBPATH', def_value=get_abs_path('~/.smmdbstore'))

INIT_STATE = {
    DATA_ID: {},
    GROUP_ID: [],
    COUNT_ID: 0,
    OWNER_ID: "anonymous"
}


class SmmDBCorrupted(Exception):
    pass


class SmmDBKeyError(Exception):
    pass


class SmmDBKeyDuplicate(Exception):
    pass


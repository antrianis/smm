import json
import uuid

from smm.utils import check_configuration
from smm.utils import is_file
from smm.utils import create_db_path
from smm.utils import init_smmdbstore
from smm.utils import copy_file
from smm.utils import get_file_name
from smm.backend_fixtures import *
from smm.api import SMMApi
from collections import OrderedDict


class SMMemory(SMMApi):

    def __init__(self, path=DB_PATH):
        self._smm_db_location = get_abs_path(
            path) if path is not None else get_abs_path(DB_DEF_PATH)
        self._smm_db = get_file_name(self._smm_db_location, DB_FILE_NAME)
        self._data = None
        if not check_configuration(self._smm_db):
            create_db_path(self._smm_db_location)
        if not is_file(self._smm_db):
            init_smmdbstore(self._smm_db, INIT_STATE)
        # by now, db is there
        self._data = self._load_json(self._smm_db)
        self._check_data_integrity()

    # helper methods ...
    def _check_data_integrity(self):
        if not all((False if self._data.get(DATA_ID) is None else True,
                    False if self._data.get(GROUP_ID) is None else True,
                    False if self._data.get(COUNT_ID) is None else True)):
            raise SmmDBCorrupted('Data file corrupted!')
        all_commands = self.list_all()
        total = len(all_commands)
        if total != self._data[COUNT_ID]:
            print 'Repairing counter integrity ...',
            self._data[COUNT_ID] = total
            self._write_db()
            print 'Done'

    def _load_json(self, path):
        with open(path, 'r') as fp:
            try:
                return json.load(fp)
            except ValueError:
                raise SmmDBCorrupted('Data file corrupted!')

    def _write_db(self):
        try:
            copy_file(self._smm_db,
                      get_file_name(self._smm_db_location, DB_FILE_NAME_BKP))
            with open(self._smm_db, 'w+') as outfile:
                json.dump(self._data, outfile, indent=2, sort_keys=True)
        except (OSError, IOError):
            raise OSError('Unable to save data to disk.')

    def _match_candidates(self, all_commands, search_items, criteria):
        matched_commands = OrderedDict()
        for command_id, command in all_commands.iteritems():
            if criteria.lower() == 'or':
                for search_item in search_items:
                    if search_item in command.get(
                            COMM_TEXT,
                            '') and command_id not in matched_commands.keys():
                        matched_commands[command_id] = command
            elif criteria.lower() == 'and':
                if set(search_items).issubset(
                        command.get(COMM_TEXT),
                        '') and command_id not in matched_commands.keys():
                    matched_commands[command_id] = command
        return matched_commands
    # helper methods

    def list_all(self, data=None):
        data = data if data is not None else self._data
        all_commands = OrderedDict()
        all_groups = data.get(GROUP_ID, [])
        for group in all_groups:
            group_commands = data.get(DATA_ID, {}).get(group, {})
            for command_id, value in group_commands.iteritems():
                all_commands[command_id] = value
        return all_commands

    def get_number_of_commands(self):
        try:
            return int(self._data.get(COUNT_ID))
        except (KeyError, ValueError):
            raise SmmDBCorrupted('Cannot find counter value.')

    def get_number_of_groups(self):
        return len(self._data.get(GROUP_ID, []))

    def find_commands(self, search_txt, criteria='or'):
        all_commands = self.list_all()
        matched_commands = self._match_candidates(
            all_commands,
            search_txt.split(),
            criteria)
        return matched_commands

    def find_command_group(self, group_name, search_txt, criteria='or'):
        all_group_commands = self._data.get(DATA_ID, {}).get(group_name, {})
        matched_commands = self._match_candidates(
            all_group_commands,
            search_txt.split(),
            criteria)
        return matched_commands

    def list_command_group(self, group_name):
        return self._data.get(DATA_ID, {}).get(group_name, {})

    def add_command(self, group, command_text, description, uid=None):
        if group not in self._data.get(GROUP_ID):
            self.create_command_group(group)
        group_commands = self._data.get(DATA_ID).get(group)
        uid = str(uid) if uid is not None else str(uuid.uuid4())
        group_commands[uid] = {COMM_DESC: description,
                               COMM_TEXT: command_text,
                               COMM_GROUP: group}
        self._data[COUNT_ID] += 1
        self._write_db()

    def list_all_groups(self, data=None):
        data = data if data is not None else self._data
        return data.get(GROUP_ID, [])

    def delete_command(self, cmd_id):
        all_commands = self.list_all()
        if cmd_id not in all_commands.keys():
            raise SmmDBKeyError('Wrong key: ' + str(cmd_id))
        group_name = all_commands.get(cmd_id).get(COMM_GROUP)
        ret_val = self._data.get(DATA_ID).get(group_name).pop(cmd_id)
        self._data[COUNT_ID] -= 1
        self._write_db()
        return ret_val

    def delete_command_group(self, group_name):
        if group_name not in self._data.get(GROUP_ID, []):
            raise SmmDBKeyError('Wrong key: ' + str(group_name))
        self._data.get(GROUP_ID).remove(group_name)
        existing_commands = len(self._data.get(DATA_ID).get(group_name).keys())
        self._data[COUNT_ID] -= existing_commands
        ret_val = self._data.get(DATA_ID).pop(group_name)
        self._write_db()
        return ret_val

    def create_command_group(self, group_name):
        if group_name in self._data.get(GROUP_ID):
            raise SmmDBKeyDuplicate('Duplicated key: ' + str(group_name))
        self._data.get(GROUP_ID).append(group_name)
        self._data.get(DATA_ID)[group_name] = {}
        self._write_db()
        return group_name

    def import_db(self, path):
        new_db_abs_path = get_abs_path(path)
        imported = self._load_json(new_db_abs_path)
        total = 0
        for group in self.list_all_groups(data=imported):
            commands = imported.get(DATA_ID, {}).get(group, {})
            for key, command in commands.iteritems():
                self.add_command(group,
                                 command.get(COMM_TEXT),
                                 command.get(COMM_DESC),
                                 key)
                total += 1
        return total

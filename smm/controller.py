from smm.utils import logger, get_parts_delimeter_quoted, user_yes_no_query
import pyperclip
from smm.view import ColorfulAsciiDisplay, ColorTerminalPrinter
from smm.backend import SMMemory
from smm.backend_fixtures import SmmDBKeyError
import sys


class SMMCommand(object):

    def __init__(self, op, text, group, description):
        self.op = op
        self.text = text
        self.group = group
        self.description = description

    def __eq__(self, other):
        return (
            isinstance(
                other,
                self.__class__) and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class SMMController(object):

    def __init__(
            self,
            smm_backend=SMMemory(),
            display=ColorfulAsciiDisplay(ColorTerminalPrinter),
            wait_for_user_input=True):
        self.smm_display = display
        self.smm_backend = smm_backend
        self.wait_for_user_input = wait_for_user_input

    def construct_smm_command(self, allargs):
        """
            returns op, text, category, description from str
            by splitting the parameter based on the delimeter
        """
        parts = get_parts_delimeter_quoted(allargs)
        allowed_ops = ['S', 'A', 'D']
        op, text, group, description = parts + [''] * (4 - len(parts))
        op = 'S' if not op else op
        try:
            op = str(op).upper()
            if op not in allowed_ops:
                raise ValueError
        except ValueError:
            # TODO: StringIO
            print 'Invalid value. Operations supported are:',\
                ','.join(allowed_ops)

        logger.debug(
            'op: {} text: {} group: {} description: {}'.format(
                op,
                text,
                group,
                description))

        return SMMCommand(op, text, group, description)

    def do_search(self, smm_cmd):
        search_text, group = smm_cmd.text, smm_cmd.group

        self.smm_display.display_db_stats_header(
            self.smm_backend.get_number_of_commands(),
            self.smm_backend.get_number_of_groups())

        if search_text and not group:
            res = self.smm_backend.find_commands(search_text)
        elif search_text and group:
            res = self.smm_backend.find_command_group(
                group,
                search_text)
        elif not search_text and not group:
            self.smm_display.display_all_groups_header(
                self.smm_backend.list_all_groups())
            res = self.smm_backend.list_all()
        elif not search_text and group:
            res = self.smm_backend.list_command_group(group)
        else:
            raise NotImplementedError

        self.smm_display.process_smm_cmd(res)
        self.smm_display.display_footer(
            self.smm_backend.get_number_of_commands())

    def do_add(self, smm_cmd):
        if smm_cmd.text and smm_cmd.group:
            self.smm_backend.add_command(
                smm_cmd.group,
                smm_cmd.text,
                smm_cmd.description)
        elif not smm_cmd.text and smm_cmd.group:
            self.smm_backend.create_command_group(smm_cmd.group)
        else:
            raise NotImplementedError

    def process_ui_search(self):
        print 'Enter index or enter to exit: ',
        inp = raw_input()
        try:
            inp = int(inp)
            if inp < 0 or inp >= len(self.smm_display.state):
                raise IndexError
        except IndexError:
            print 'Index out of range'
        except ValueError:
            if not inp:
                # user pressed enter
                return
            print 'Ilegal selection'
        else:
            pyperclip.copy(self.smm_display.state[inp][1])

    def process_ui_delete(self):
        print 'Enter index, group name or enter to exit: ',
        inp = raw_input()
        try:
            inp = int(inp)
            if inp < 0 or inp >= len(self.smm_display.state):
                raise IndexError
        except IndexError:
            print 'Index out of range'
        except ValueError:
            if not inp:
                # user pressed enter
                return
            try:
                if user_yes_no_query(
                        'Are you sure you want to delete group %s' %
                        inp):
                    self.smm_backend.delete_command_group(str(inp))
                else:
                    return
            except SmmDBKeyError as key_error:
                print key_error
        else:
            to_delete = self.smm_display.state[inp][0]
            self.smm_backend.delete_command(to_delete)

    def process_smm_cmd(self, smm_cmd):

        try:
            if smm_cmd.op == 'A':
                self.do_add(smm_cmd)
            elif smm_cmd.op in ['D', 'S']:
                self.do_search(smm_cmd)

            if self.wait_for_user_input and sys.stdout.isatty():
                if smm_cmd.op == 'S':
                    self.process_ui_search()
                elif smm_cmd.op == 'D':
                    self.process_ui_delete()
        except OSError as oserror:
            print oserror

    def exec_main(self, allargs):
        smm_cmd = self.construct_smm_command(allargs)
        self.process_smm_cmd(smm_cmd)

    def import_db(self, sourcefile):
        self.smm_backend.import_db(sourcefile)

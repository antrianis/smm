class SMMApi(object):
    """API"""
    # dont delete it, leave it for now

    def list_all(self):
        """Return all commands
        Examples:
        {'id1': {'text': 'ls -l', 'desc': 'List files', 'group': 'bash'}}
        {}

        :return: All available commands
        :rtype: dict
        """
        raise NotImplementedError

    def find_commands(self, search_txt, criteria='or'):
        """Return all commands that match search text and given criteria

        :param str search_txt: Search terms space separated
        :param str criteria: Search criteria ('or' gives all commands that match any word,
        'and' returns commands that match all words, 'alike' returns approximate matches)
        :return: Commands that satisfy search criteria
        :rtype: tuple
        """
        raise NotImplementedError

    def find_command_group(self, group_name, search_txt, criteria='or'):
        """Return all commands that match search text and given criteria in the group

        :param str group_name: Group name
        :param str search_txt: Search terms space separated
        :param str criteria: Search criteria ('or' gives all commands that match any word,
        'and' returns commands that match all words, 'alike' returns approximate matches)
        :return: Commands that satisfy search criteria
        :rtype: dict
        """
        raise NotImplementedError

    def get_number_of_groups(self):
        """Return total number of commands

        :return: Number of commands
        :rtype: int
        """
        raise NotImplementedError

    def get_number_of_commands(self):
        """Return number of groups

        :return: Number of groups
        :rtype: int
        """
        raise NotImplementedError

    def list_all_groups(self):
        """Return list of all groups

        :return: List of groups
        :rtype: list
        """
        raise NotImplementedError

    def list_command_group(self, group_name):
        """Return all commands from the group

        :param group_name: Group name
        :return: Commands from the group
        :rtype: dict
        """
        raise NotImplementedError

    def add_command(self, group, command_text, description):
        """Add command to specific group. Create a group if doesn't exist

        :param str group: Group name
        :param str command_text: Text of command
        :param str description: Description
        :raises: OSError, SmmDBKeyDuplicate
        """
        raise NotImplementedError

    def delete_command(self, cmd_id):
        """Delete command with given id

        :param str cmd_id: Command id
        :return: Deleted command
        :rtype: dict
        :raises: OSError, SmmDBKeyError
        """
        raise NotImplementedError

    def delete_command_group(self, group_name):
        """Delete command group

        :param str group_name: Command name
        :return: Deleted group of commands
        :raises: OSError, SmmDBKeyError
        """
        raise NotImplementedError

    def create_command_group(self, group_name):
        """Create command group

        :param str group_name: Command group name
        :return: Created group name
        :raises: OSError, SmmDBKeyDuplicate
        """
        raise NotImplementedError

    def import_db(self, path):
        """Import a smm dbstore

        :param str path: Path to the data file
        :return:
        """
        raise NotImplementedError

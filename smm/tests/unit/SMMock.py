from smm.api import SMMApi


class SMMock(SMMApi,):

    def __init__(self, dppath):
        pass

    def list_all(self):
        dict_smm = {}
        dictA, dictB = {}, {}
        dictA['desc'] = 'return the config'
        dictA['group'] = 'git'
        dictA['text'] = 'git config'
        dictB['desc'] = 'searching'
        dictB['group'] = 'bash'
        dictB['text'] = 'find . txt'
        dict_smm[100] = dictA
        dict_smm[101] = dictB
        return (True, dict_smm)

    def get_number_of_groups(self):
        return 3

    def get_number_of_commands(self):
        return 10

    def find_commands(self, search_txt):
        """ returns all commands that match the text"""
        dict_smm = {}
        dictA = {}
        dictA['desc'] = 'return the config'
        dictA['group'] = 'git'
        dictA['text'] = 'git config'
        dict_smm[100] = dictA
        return (True, dict_smm)

    # again a dict always a dict
    def find_command_group(self, group_name, search_txt):
        dict_smm = {}
        dictA = {}
        dictA['desc'] = 'return the config'
        dictA['group'] = 'git'
        dictA['text'] = 'git config'
        dict_smm[100] = dictA
        return (True, dict_smm)

    # only this one is a list
    def list_all_groups(self):
        return (True, ['git', ])
    # a dict

    def list_command_group(self, group_name):
        dict_smm = {}
        dictA = {}
        dictA['desc'] = 'return the config'
        dictA['group'] = 'git'
        dictA['text'] = 'git config'
        dict_smm[100] = dictA
        return (True, dict_smm)

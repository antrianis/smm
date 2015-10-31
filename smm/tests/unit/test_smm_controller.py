import unittest
from smm.controller import SMMController, SMMCommand


class SMMTestController(unittest.TestCase):

    def setUp(self):
        self.controller = SMMController()

    def test_smm_command(self):

        smm_cmd = SMMCommand('S', 'a cmd', 'test_group', 'descr')
        assert smm_cmd.op == 'S' and smm_cmd.group == 'test_group' and\
            smm_cmd.description == 'descr' and smm_cmd.text == 'a cmd'

#     def test_invalid_construct_smm_command(self):
#         self.assertRaises(
#             ValueError,
#             self.controller.construct_smm_command, "k")
# 
#         self.assertRaises(
#             ValueError,
#             self.controller.construct_smm_command, "1")

    def test_construct_smm_command_add(self):
        self.assertEqual(
            SMMCommand(
                'A',
                'test',
                'groupname',
                ''),
            self.controller.construct_smm_command("a/test/groupname"))

        self.assertEqual(
            SMMCommand(
                'A',
                '',
                'groupname',
                ''),
            self.controller.construct_smm_command("a//groupname"))

    def test_construct_smm_command_delete(self):
        self.assertEqual(
            SMMCommand(
                'D',
                's',
                '',
                ''),
            self.controller.construct_smm_command("d/s"))

        self.assertEqual(
            SMMCommand(
                'D',
                '',
                '',
                ''),
            self.controller.construct_smm_command("d/"))

        self.assertEqual(
            SMMCommand(
                'D',
                'test',
                'groupname',
                ''),
            self.controller.construct_smm_command("d/test/groupname"))

        self.assertEqual(
            SMMCommand(
                'D',
                'test',
                'groupname',
                ''),
            self.controller.construct_smm_command("d/test/groupname"))

        self.assertEqual(
            SMMCommand(
                'D',
                '',
                'groupname',
                ''),
            self.controller.construct_smm_command("d//groupname"))

        self.assertEqual(
            SMMCommand(
                'D',
                '',
                '',
                ''),
            self.controller.construct_smm_command("d"))

    def test_construct_smm_command_search(self):

        self.assertEqual(
            SMMCommand(
                'S',
                's',
                '',
                ''),
            self.controller.construct_smm_command("/s"))

        self.assertEqual(
            SMMCommand(
                'S',
                's',
                '',
                ''),
            self.controller.construct_smm_command("s/s"))

        self.assertEqual(
            SMMCommand(
                'S',
                '',
                '',
                ''),
            self.controller.construct_smm_command("s"))

        self.assertEqual(
            SMMCommand(
                'S',
                '',
                '',
                ''),
            self.controller.construct_smm_command(""))

        self.assertEqual(
            SMMCommand(
                'S',
                'test',
                'groupname',
                ''),
            self.controller.construct_smm_command("/test/groupname"))

        self.assertEqual(
            SMMCommand(
                'S',
                'test',
                'groupname',
                ''),
            self.controller.construct_smm_command("/test/groupname"))

        self.assertEqual(
            SMMCommand(
                'S',
                '',
                'groupname',
                ''),
            self.controller.construct_smm_command("//groupname"))

import unittest
from smm.view import ColorfulAsciiDisplay, UncoloredPrinter
from mock.mock import patch
from StringIO import StringIO


class SMMTestView(unittest.TestCase):

    def setUp(self):
        self.view = ColorfulAsciiDisplay(UncoloredPrinter)

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_header(self, mock_stdout):
        self.view.display_db_stats_header(10, 20)
        assert mock_stdout.getvalue(
        ) == 'Total Commands: 10 Total Groups: 20\n'

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_display_all_groups_header_empty(self, mock_stdout):
        self.view.display_all_groups_header([])
        assert mock_stdout.getvalue() == 'Groups: \n'

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_display_all_groups_header(self, mock_stdout):
        self.view.display_all_groups_header(['G1', 'G2'])
        assert mock_stdout.getvalue() == 'Groups: G1, G2\n'

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_display_footer(self, mock_stdout):
        self.view.display_footer(0)
        assert mock_stdout.getvalue() == 'Result%: 0.00\n'

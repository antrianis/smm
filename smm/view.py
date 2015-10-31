from blessed import Terminal
from smm.backend_fixtures import COMM_DESC, COMM_GROUP, COMM_TEXT
import warnings
from smm.utils import len_cap


class DisplayBehavior(object,):
    state = []

    def process_smm_cmd(self, dct):
        raise NotImplementedError


class PrintObj(object):

    def __init__(self, text, color=None):
        self.color = color
        self.text = text


class ColorTerminalPrinter(object):

    def __init__(self, t):
        self.t = t

    def output(self, print_obj):
        for obj in print_obj:
            if obj.color is not None:
                print self.t.__getattr__(obj.color)(obj.text),
            else:
                print obj.text,
        print


class UncoloredPrinter(object):

    def __init__(self, t):
        self.t = t

    def output(self, print_obj):
        for obj in print_obj:
            print obj.text,
        print


class ColorfulAsciiDisplay(DisplayBehavior):

    def __init__(self, printer):
        # surpress blessed pkg warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.t = Terminal()
            self.printer = printer(self.t)

    def display_db_stats_header(self, no_cmds, no_groups):
        self.printer.output([PrintObj('Total Commands:',
                                      'green'),
                             PrintObj(no_cmds),
                             PrintObj('Total Groups:',
                                      'green'),
                             PrintObj(no_groups)],)

    def display_all_groups_header(self, all_groups):
        self.printer.output(
            [PrintObj('Groups:', 'green'), PrintObj(', '.join(all_groups))])

    def display_footer(self, total_cmds):
        res_percent = len(
            self.state) / float(total_cmds) if total_cmds > 0 else 0

        percentage = "%.2f" % (res_percent * 100)
        self.printer.output(
            [PrintObj('Result%:', 'green'), PrintObj(percentage)])

    def process_smm_cmd(self, dct):
        term_width = self.t.width
        self.state = []

        a = int(term_width * 0.05)
        b = int(term_width * 0.10)
        c = int(term_width * 0.60)
        d = int(term_width * 0.25)

        title = "%-*s%-*s%-*s%-*s" % (a, 'i',
                                      c, 'Command',
                                      b, 'Group',
                                      d, 'Description',
                                      )
        self.printer.output([PrintObj(title, 'bold_black_on_bright_green')])

        for index, key in enumerate(dct):
            vals = dct[key]
            self.state.append((key, vals[COMM_TEXT]))
            cmd = "%-*s%-*s%-*s%-*s" % (a, index,
                                        c, len_cap(vals[COMM_TEXT], c - 1),
                                        b, len_cap(vals[COMM_GROUP], b - 1),
                                        d, len_cap(vals[COMM_DESC], d - 1),
                                        )
            self.printer.output([PrintObj(cmd)])


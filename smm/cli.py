#!/usr/bin/env python

import click
from smm.backend_fixtures import SmmDBCorrupted
import sys
from smm.controller import SMMController
from smm.utils import configure_logger


__version__ = '0.1'


@click.command()
@click.argument('allargs', nargs=1, default="", type=str)
@click.option('--sourcefile', '-s', default='')
@click.option('--version', '-v', help='Version', is_flag=True)
@click.option('logging_level',
              '-l',
              help='Logging level',
              default='INFO',
              type=click.Choice(['DEBUG',
                                 'INFO',
                                 'WARN',
                                 'ERROR']))
def sm_main(allargs, version, sourcefile, logging_level):
    """
    search operation/text/category/description
    e.g.
    /ls/bash/
    operation = d,a,s default is s
    """
    configure_logger(logging_level)
    if version:
        print __version__
        exit()
    try:
        smm_controller = SMMController()
    except SmmDBCorrupted as dbcorr:
        print dbcorr
        raise

    if sourcefile:
        smm_controller.import_db(sourcefile)
        exit()

    failed = 'illegal options. run with --help for usage'

    try:
        smm_controller.exec_main(allargs)
    except NotImplementedError:
        print failed
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        raise

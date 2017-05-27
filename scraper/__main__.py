#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI handler.
"""

import argparse
import signal
import sys

from commands import available_commands, handle_command

PROGRAM_NAME = 'scraper'

description = f'''
Crawl and scrape dynamic Web sites.
Scrape Web sites that dynamically load content or
sites that render their HTML using javascript.
Either use the command pattern provided or
import "{PROGRAM_NAME}" to use as a library.
'''


def get_parser():
    parser = argparse.ArgumentParser(
        description=description,
        prog=PROGRAM_NAME,
    )
    parser.add_argument('command', type=str, help='The command to run.', choices=available_commands())
    return parser


def main():
    # parse args
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:2])
    command = args.command

    if command:
        handle_command(command, parser)


if __name__ == '__main__':
    # Config stuff
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # sys.excepthook = lambda et, e, tb: print(f'{et.__name__}: {e}')

    # Start the main program
    main()

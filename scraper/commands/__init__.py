""" Command Pattern

Functions to fetch or execute the available commands.
"""
import argparse
import os
import sys
from importlib import import_module


def handle_command(command, parser):
    """ Executes a command.
    Args:
        command (str): Name of the command.
        parser (ArgumentParser): The Schireson program's parser.
    """
    command_dict = get_commands()

    # get command options
    parser = argparse.ArgumentParser(parents=[parser], add_help=False)
    command_dict[command].add_arguments(parser)
    args = parser.parse_args(sys.argv[1:])

    # execute command
    command_dict[command].execute(args)


def available_commands():
    """ All available commands.
    Returns:
        ([str]) Names of the available commands.
    """
    commands_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isdir(commands_dir):
        raise Exception(f'Cannot find "commands" directory at {commands_dir}')

    return [
        name.split('.')[0]
        for name in os.listdir(commands_dir)
        if name.endswith('.py') and not name.startswith('_')
    ]


def get_commands():
    """ Command names mapped to an instance of that command.
    Returns:
        (dict) mapping {<command_file_name>: <command.Command()>}
    """
    commands = available_commands()
    return {
        name: import_module(
            f'commands.{name}'
        ).Command()
        for name in commands
    }

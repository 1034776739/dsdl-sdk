"""

Examples:

class Example(CmdBase):
    def init_parser(self, subparsers):
        status_parser = subparsers.add_parser('example', help='Show the working tree status')
        status_parser.add_argument('show', nargs='?', default='SHOW', help='show example')
        return status_parser

    def cmd_entry(self, args, config):
        print(args)
        print(config)

"""
from abc import ABC, abstractmethod
from argparse import _SubParsersAction, ArgumentParser


class CmdBase(ABC):
    """
    Base class for all commands

    Args:
        ABC:

    Returns:

    """

    @abstractmethod
    def cmd_entry(self, args, config):
        """
        Entry point for the command

        Args:
            self:
            args:
            config:

        Returns:

        """
        raise NotImplementedError

    @abstractmethod
    def init_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        """
        Initialize the parser for the command

        Args:
            self:
            subparsers:

        Returns:

        """
        raise NotImplementedError

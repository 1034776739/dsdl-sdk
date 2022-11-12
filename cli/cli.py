"""

References:
    https://developer.aliyun.com/article/740160
    https://docs.python.org/zh-cn/3/library/argparse.html
"""
import argparse
import os.path
import sys
from commands.cmdbase import CmdBase
import importlib
import inspect
from pathlib import Path
from commands.__version__ import __version__
from commands.const import PROG_NAME
from commons.argument_parser import DsdlArgumentParser as ArgumentParser
# from argparse import ArgumentParser

from commons.argument_parser import CustomHelpFormatter

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DSDLClient(object):
    """
    DSDL 命令行客户端
    """

    def __init__(self):
        """
        初始化命令行客户端
        """
        self.__config = self.__init_cli_config()
        self.__parser = ArgumentParser(prog=PROG_NAME,
                                       description="""
            Use 'dsdl <command>' to access/load datasets either from local 
            file system or remote cloud storage, can also perform data-preprocessing
            including filtering, visualization, etc.
                                                """,
                                       epilog="Report bugs to https://github.com/opendatalab/dsdl-sdk/issues",
                                       usage=f"{PROG_NAME} GLOBAL_FLAGS | COMMAND [COMMAND_ARGS] [DATASET_NAME]",
                                       formatter_class=CustomHelpFormatter,
                                       # example = "dsdl -h",
                                       )
        self.__subparsers = self.__parser.add_subparsers(
            title="Commands",
            )
        self.__init_subcommand_parser()

        self.__init_global_flags()  # 初始化全局参数
        self.__args = self.__parser.parse_args()

    def execute(self):
        """
        执行命令
        Returns:

        """
        if hasattr(self.__args, 'command_handler'):
            self.__args.command_handler(self.__args, self.__config)
        else:
            self.__parser.print_usage()

    def __init_cli_config(self):
        """
        TODO 初始化命令行配置

        Returns:

        """
        # 检查配置文件是否存在，如果没有则创建一个
        # 检查sqlite数据库是否存在，如果没有则创建一个
        # 检查sqlite数据库是否有表，如果没有则创建表

        return None

    def __init_global_flags(self):
        """
        初始化默认参数
        Returns:

        """
        self.__parser._optionals.title = "Global flags"
        self.__parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}', help='show the DSDL cli version and exit.')

    def __init_subcommand_parser(self):
        """
        此处初始化子命令解析器。

        过程是扫描commands目录里集成了CmdBase的子类，然后
        Args:
            subcommand:
            help:

        Returns:

        """
        import commands

        pkgs = [
            module.stem
            for module in Path(commands.__path__[0]).iterdir()
            if module.is_file() and module.suffix == '.py' and not module.name.startswith('_')
        ]  # 获取commands目录下的所有py文件
        for pkg in pkgs:
            module = importlib.import_module(f'commands.{pkg}')
            for clz_name, clz_obj in inspect.getmembers(module):
                if inspect.isclass(clz_obj) and issubclass(clz_obj, CmdBase) and not inspect.isabstract(clz_obj):
                    cmd_clz = clz_obj()
                    subcmd_parser = cmd_clz.init_parser(self.__subparsers)
                    subcmd_parser.set_defaults(command_handler=cmd_clz.cmd_entry)
                    subcmd_parser._optionals.title = "Command args"


if __name__ == '__main__':
    DSDLClient().execute()

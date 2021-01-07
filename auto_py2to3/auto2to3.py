#!/usr/bin/python3
# -*- coding: utf-8 -*-
# auto_py2to3 is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# Create: 2020-8-1

"""Main module."""
import os
import click
from utils import *
import prettytable as pt


@click.command()
@click.option(
    '-interpreter_command_name',
    default="python",
    help='(str)The global command name of the Python interpreter, used in order to execute 2to3.'
)
@click.option(
    '-project_path',
    default="",
    # prompt='Transfer Folder/File Path',
    help='(str)Must Give A Transfer Folder/File Path.'
)
@click.option(
    '-is_del_bak',
    default=0,
    help='(1/0)The global command name of the Python interpreter, used in order to execute 2to3.'
)
@click.option(
    '-verify_library_version',
    # prompt='Requirement Library File Path',
    default="",
    help='(str)Only the standard requirements.txt version control format is supported.'
)
def auto_2to3(interpreter_command_name, project_path, is_del_bak, verify_library_version):
    """Auto 2to3 Tool Usage Command Description"""
    if project_path:
        for file_path in find_all_py_files(path=project_path):
            print(os.system(f'{interpreter_command_name} libs/2to3.py -w {file_path}'))
    if is_del_bak:
        del_bak(path=project_path)
    if verify_library_version:
        print("Current Python Version: {0}.".format(sys.version))
        verify_result = pt.PrettyTable(['No', 'Library', 'Version', 'Support Status', 'Recommend Version'])
        python_version = float("{0}.{1}".format(sys.version_info.major, sys.version_info.minor))
        print("Statistical analysis of dependent libraries to adapt to the current Python version: Loading...")
        for i, (ln, versions) in enumerate(find_python_versions_by_library_versions(
            get_requirements_library(path=verify_library_version)
        ).items()):
            if python_version in versions["python_version"]:
                verify_result.add_row([str(i + 1), ln, versions["version"], '√', versions["version"]])
            else:
                verify_result.add_row([str(i + 1), ln, versions["version"], '×', versions["newest_version"]])
        print(verify_result)
    return True


if __name__ == '__main__':
    """
    test command: python auto2to3.py -verify_library_version ../tests/example1/requirements.txt
    """
    try:
        auto_2to3()
    except SystemError as e:
        print(e)
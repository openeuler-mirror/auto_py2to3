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
from utils import find_all_py_files, del_bak


@click.command()
@click.option('--interpreter_command_name', default="python",
              help='(str)The global command name of the Python interpreter, used in order to execute 2to3.')
@click.option('--project_path', prompt='Transfer Folder/File Path', help='(str)Must Give A Transfer Folder/File Path.')
@click.option('--is_del_bak', default=0,
              help='(1/0)The global command name of the Python interpreter, used in order to execute 2to3.')
def auto_2to3(interpreter_command_name, project_path, is_del_bak):
    """Auto 2to3 Tool Usage Command Description"""
    for file_path in find_all_py_files(path=project_path):
        print(os.system(f'{interpreter_command_name} libs/2to3.py -w {file_path}'))
    if is_del_bak:
        del_bak(path=project_path)
    return True


if __name__ == '__main__':
    """
    test command: python3.6 auto2to3.py ../tests/test_project
    """
    try:
        auto_2to3()
    except Exception as e:
        print(e)

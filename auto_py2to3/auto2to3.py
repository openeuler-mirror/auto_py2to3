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

from .pylibrary import *
from .pyfiles import *

__all__ = ["py2to3"]


def py2to3(target_path,
           interpreter_command_name="python",
           is_transform=False,
           is_del_bak=False,
           is_html_diff=False,
           is_check_requirements=False):
    """
    The main entrance of the 2to3 function provides a series of parameter entrances.
    The main functions are as follows:
        1. Whether to enable automatic conversion of Python2 code to Python3
        2. Determine whether to keep a backup of Python2 code
        3. Determine whether to open the conversion code text comparison
        4. Determine whether the version of the library that the project
           depends on is suitable for the current Python environment.

    :param target_path:
           str, project path
    :param interpreter_command_name:
           str, interpreter command name, default "python"

           Please make sure that the Python terminal environment
           has been configured successfully
    :param is_transform:
           bool, default False
    :param is_del_bak:
           bool, default False
    :param is_html_diff:
           bool, default False
    :param is_check_requirements:
           bool, default False
    :return: bool, ignore
    """
    # Whether to enable automatic conversion of Python2 code to Python3
    if is_transform:
        files_transform(
            target_path=target_path,
            interpreter_command_name=interpreter_command_name
        )
    # Determine whether to keep a backup of Python2 code
    if is_del_bak:
        bak_files_clear(target_path=target_path)
    # Determine whether to open the conversion code text comparison
    if is_html_diff:
        html_diff_generate(target_path=target_path)
    # Determine whether the version of the library that the project
    # depends on is suitable for the current Python environment.
    if is_check_requirements:
        libraries_detect_and_recommend(target_path=target_path)
    return True


def test():
    """
    Unit test function for the main entrance of the local test 2to3 function

    :return: bool, ignore
    """
    try:
        py2to3(
            target_path="../tests/ticketGrabbingExample",
            interpreter_command_name="python",
            is_transform=False,
            is_del_bak=False,
            is_html_diff=False,
            is_check_requirements=True
        )
    except SystemError as e:
        print(e)
    return True


if __name__ == '__main__':
    pass
    # test()

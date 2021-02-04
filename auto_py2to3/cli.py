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
# Create: 2021-2-1

import click
from auto2to3 import py2to3


@click.command()
@click.option(
    "--path", "-p",
    prompt="Transfer Folder/File Path",
    help="(str)Must Give A Transfer Folder/File Path."
)
@click.option(
    "--interpreter_command_name", "-i",
    default="python",
    help="(str)The global command name of the Python interpreter, used in order to execute 2to3."
)
@click.option(
    "--is_transform", "-t",
    default=0,
    help="(1/0)Whether to convert the specified project code."
)
@click.option(
    "--is_del_bak", "-d",
    default=0,
    help="(1/0)Whether to delete the original Python file after conversion."
)
@click.option(
    "--is_html_diff", "-h",
    default=0,
    help="(1/0)Whether to generate an HTML comparison file of the converted Python file."
)
@click.option(
    "--is_check_requirements", "-r",
    default=0,
    help="(1/0)Whether to check the version of the dependent library related to requirements.txt in the project."
)
def main(path,
         interpreter_command_name,
         is_transform,
         is_del_bak,
         is_html_diff,
         is_check_requirements):
    """

    :param path:
    :param interpreter_command_name:
    :param is_transform:
    :param is_del_bak:
    :param is_html_diff:
    :param is_check_requirements:
    :return:

    Example:
    ---------
        python cli.py -p ../tests/ticketGrabbingExample -i python -t 1 -d 0 -h 1 -r 1
    """
    return py2to3(
        target_path=path,
        interpreter_command_name=interpreter_command_name,
        is_transform=is_transform,
        is_del_bak=is_del_bak,
        is_html_diff=is_html_diff,
        is_check_requirements=is_check_requirements
    )


if __name__ == "__main__":
    main()

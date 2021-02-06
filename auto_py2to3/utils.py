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

import re
from datetime import datetime
from pathlib import Path
from pprint import pprint

# print = pprint
print = print


def is_number(num_str):
    """
    Determine whether the string can be converted to a number (int and float)
    :param num_str:
    :return:
    """
    if not re.compile(r"^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$").match(num_str):
        return False
    return True


def format_date_en2standard(date, en_fmt, return_type="str"):
    """
    Specify English format date string conversion standard string structure

    Example:

    en_fmt:
        "Friday, November 18, 2016" -> "%A, %B %d, %Y"

            %a abbreviated English week
            %A Complete English week
            %b Shorthand for English month
            %B complete English month
            %c displays local date and time
            %d date, take 1-31
            %H hours, 0-23
            %I hours, 0-12
            %m month, 01 -12
            %M minutes, 1-59
            %j number of days in the year
            %w shows what day is today
            %W Week
            %x today"s date
            %X local time of day
            %y year 00-99
            %Y full spelling of the year

    :param date:
    :param en_fmt:
    :param return_type:
            str
            timeObject
    :return:
    """
    if return_type == "str":
        try:
            return datetime.strptime(date, en_fmt).strftime("%Y-%m-%d")
        except SyntaxError as e:
            print(e)
        return ""
    elif return_type == "timeObject":
        try:
            return datetime.strptime(date, en_fmt)
        except SyntaxError as e:
            print(e)
        return None
    else:
        raise ValueError("Do not Support ({0}) Type Parameter!".format(return_type))


def find_files(path, pattern="*"):
    """
    Get all files under this path

    :param path: files dir
    :param pattern:
        All files are returned by default, and the file type can also be customized,
        for example: pattern="*.py"
    :return:
    """
    if not Path(path).is_dir():
        print("The path params is not dir, no files can be found!")
        return []
    return [str(file.resolve()) for file in Path(path).rglob(pattern) if Path(file).is_file()]

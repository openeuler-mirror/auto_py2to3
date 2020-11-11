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


import os
import sys
import requests
import re

WIN = sys.platform.startswith('win')
if WIN:
    path_split = '\\'
else:
    path_split = '/'


def find_all_py_files(path):
    """
    Get all py files under this path
    :param path:
    :return:
    """
    for base_path, dir_names, file_names in os.walk(path):
        for real_path in [
            os.path.join(base_path, p).replace(path_split, "/") for p in dir_names + file_names if ".py" in p
        ]:
            if real_path:
                yield real_path


def del_bak(path):
    """
    Absolute path to the target project folder
    :param path:
    :return:
    """
    for base_path, dir_names, file_names in os.walk(path):
        for real_path in [
            os.path.join(base_path, p).replace(path_split, "/") for p in dir_names + file_names if ".bak" in p
        ]:
            if real_path:
                os.remove(real_path)
    return True


def _is_number(num_str):
    """
    Determine whether the string can be converted to a number (int and float)
    :param num_str:
    :return:
    """
    if not re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$').match(num_str):
        return False
    return True


def find_python_version_by_library_version(ln, lv):
    """
    Get the Python version applicable to the specified dependent library
    :param ln:
    :param lv:
    :return:
    """
    return [
        float(_) for _ in
        set(re.findall("Python :: (.*?)\n", requests.get(url=f"https://pypi.org/project/{ln}/{lv}").text))
        if _is_number(_)
    ]


def get_requirements_library(path):
    """
    Get all the dependent libraries in the specified requirements.txt
    :param path:
    :return:
    """
    requirements_dict = {}
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            ln, *lv = line.split("==")
            if not lv:
                requirements_dict[ln] = ""
            else:
                requirements_dict[ln] = lv[0]
    return requirements_dict

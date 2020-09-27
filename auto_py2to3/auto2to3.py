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
import sys

from utils import find_all_py_files


def auto_2to3(folder_path):
    for file_path in find_all_py_files(path=folder_path):
        print(os.system(r'python libs/2to3.py -w %s' % file_path))
    return True


if __name__ == '__main__':
	"""
	test command: python3.6 auto2to3.py ../tests/test_project

	"""
    try:
        path = sys.argv[1]
    except Exception as e:
        print(f"Sorry, You Must Give A Transfer Folder/File Path! Details: {e}")

    try:
        auto_2to3(path)
    except Exception as e:
        print(e)

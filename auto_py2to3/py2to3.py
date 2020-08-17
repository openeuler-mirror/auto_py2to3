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

from utils import find_all_py_files
from parse import ParsePyFiles

transfer_abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/tests/test_project/"

for file_path in find_all_py_files(path=transfer_abs_path):
    for row_content in ParsePyFiles(file_path=file_path).rows_next():
        print(row_content)

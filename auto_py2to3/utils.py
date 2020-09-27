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

WIN = sys.platform.startswith('win')
if WIN:
    path_split = '\\'
else:
    path_split = '/'


def find_all_py_files(path):
    """
    :param path:
    :return:
    """
    for base_path, dir_names, file_names in os.walk(path):
        for real_path in [
            os.path.join(base_path, p).replace(path_split, "/") for p in dir_names + file_names if ".py" in p
        ]:
            if real_path:
                yield real_path

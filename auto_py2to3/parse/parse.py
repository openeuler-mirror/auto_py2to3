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

__all__ = ['ParsePyFiles']


class ParsePyFiles(object):
    """
    解析Py文件类
    """
    def __init__(self, file_path):
        """
        读入文件内容
        :param file_path:
        """
        with open(file_path, 'r') as f:
            self.content = f.readlines()

    def rows_next(self):
        """
        遍历每一行内容
        :return:
        """
        for con in self.content:
            yield con

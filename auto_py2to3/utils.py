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
from datetime import datetime
import time
import json
import requests
import re
from collections import Counter
import deco
import random
from collections import defaultdict

WIN = sys.platform.startswith('win')
if WIN:
    path_split = '\\'
else:
    path_split = '/'


def _is_number(num_str):
    """
    Determine whether the string can be converted to a number (int and float)
    :param num_str:
    :return:
    """
    if not re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$').match(num_str):
        return False
    return True


def _format_date_en2standard(date, en_fmt, return_type='str'):
    """
    Specify English format date string conversion standard string structure

    Example:

    en_fmt:
        'Friday, November 18, 2016' -> '%A, %B %d, %Y'

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
            %x today's date
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
            return datetime.strptime(date, en_fmt).strftime('%Y-%m-%d')
        except Exception as e:
            print(e)
        return ""
    elif return_type == "timeObject":
        try:
            return datetime.strptime(date, en_fmt)
        except Exception as e:
            print(e)
        return None
    else:
        raise ValueError("Don't Support ({0}) Type Parameter!".format(return_type))


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


def update_python_versions():
    """
    Python release date configuration
    :return:
    """
    response = requests.get(url="https://www.python.org/doc/versions/").text
    match_response = re.findall("Python (.*?)</a>, documentation released on (.*?)</li>", response)
    versions = {
        "timestamp": time.time(),
        "versions": dict(
            [(_, _format_date_en2standard(en_date, '%d %B %Y')) if en_date[-1].isdigit() else (
                _, _format_date_en2standard(en_date[:-1], '%d %B %Y')) for _, en_date in
             match_response]
        )
    }
    with open("conf/python_versions.json", "w", encoding="utf-8") as f:
        json.dump(versions, f, ensure_ascii=False)
    return versions


def _version_str2tuple(vs):
    """

    :param vs:
    :return:
    """
    info = vs.split(".")
    if len(info) == 1 and _is_number(info[0]):
        return info[0], "0", "*"
    elif len(info) == 2 and all([
        _is_number(info[0]),
        _is_number(info[1])
    ]):
        return info[0], info[1], "*"
    elif len(info) == 3 and all([
        _is_number(info[0]),
        _is_number(info[1]),
        _is_number(info[2])
    ]):
        return tuple(info)
    elif len(info) == 3 and all([
        _is_number(info[0]),
        _is_number(info[1]),
        info[2] == "*"
    ]):
        return info[0], info[1], "*"
    else:
        raise ValueError()


@deco.concurrent.threaded(processes=8)
def find_python_version_by_library_version(ln, lv, update_step=30):
    """
    Get the Python version applicable to the specified dependent library
    :param update_step:  days
    :param ln:
    :param lv:
    :return:
    """
    results = {
        "version": lv,
        "python_version": [],
        "newest_version": ""
    }
    # Request detailed library version release information data
    response = requests.get(url=f"https://pypi.org/pypi/{ln}/json").json()
    newest_library_version = response.get("info", {}).get("version", "")
    results["newest_version"] = newest_library_version
    if not lv:
        print(f"Python dependency library ({ln}) does not have version.")
        return results
    # Get the timeline of Python release version
    if not os.path.exists("conf/python_versions.json"):
        # Determine whether there is a timetable cache for the Python release version
        versions = update_python_versions()["versions"]
    else:
        with open("conf/python_versions.json", "r", encoding="utf-8") as f:
            versions_dict = json.load(f)
        if (datetime.utcfromtimestamp(
            time.time()
        ) - datetime.utcfromtimestamp(
            versions_dict["timestamp"])
        ).days > update_step:
            versions = update_python_versions()["versions"]
        else:
            versions = versions_dict["versions"]

    # Calculate the exact release time of the dependent library version
    library_version_times = [
        _format_date_en2standard(
            item["upload_time_iso_8601"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ) for item in response.get("releases", {}).get(lv, [])
    ]
    if not library_version_times:
        print(f"Python dependency library ({ln}) does not have version({lv}).")
        return results
    extract_library_version_time = _format_date_en2standard(
        Counter(library_version_times).most_common(1)[0][0],
        "%Y-%m-%d",
        return_type="timeObject"
    )
    # Screening strategy:
    # 1. Time filtering according to the time of the library release version and
    # the time of the Python release version
    support_versions = [version for version, _ in filter(
        lambda x: x[1] > 0,
        [(_, (extract_library_version_time - _format_date_en2standard(
            date, "%Y-%m-%d", return_type="timeObject"
        )).days) for _, date in versions.items()]
    )]

    # 2. Filter according to the requires_python of the library release version
    requires_python = set()
    for item in response.get("releases", {}).get(lv, []):
        if item["requires_python"]:
            for _ in item["requires_python"].split(","):
                requires_python.add(_)
    for option in requires_python:
        option = option.replace(" ", "")
        if option[:2] == "!=":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    version[:3] != f"{major}.{minor}"
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    version != f"{major}.{minor}.{micro[0]}"
                ]
        elif option[:2] == ">=":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) >= float(f"{major}.{minor}")
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) >= int(f"{major}{minor}{micro[0]}")
                ]
        elif option[:2] == "<=":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) <= float(f"{major}.{minor}")
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) <= int(f"{major}{minor}{micro[0]}")
                ]
        elif option[:2] == "==":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    version[:3] == f"{major}.{minor}"
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    version == f"{major}.{minor}.{micro[0]}"
                ]
        elif option[0] == ">" and option[1].isdigit():
            major, minor, micro = _version_str2tuple(vs=option[1:])
            if not micro or micro[0] == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) > float(f"{major}.{minor}")
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) > int(f"{major}{minor}{micro[0]}")
                ]
        elif option[0] == "<" and option[1].isdigit():
            major, minor, micro = _version_str2tuple(vs=option[1:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) < float(f"{major}.{minor}")
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) < int(f"{major}{minor}{micro[0]}")
                ]
        else:
            print("other !!!!!!!!")

    # 3. Filtering according to the requirements_python of the release
    # version of the library is unsuccessful,
    # select the general version of classifiers in info to determine
    if not requires_python:
        # print("not requires_python", ln, lv)
        classifiers_versions = set()
        for item in requests.get(
            url=f"https://pypi.org/pypi/{ln}/{lv}/json"
        ).json().get("info", {}).get("classifiers", []):
            if "Python :: " in item:
                ver = item.split(" :: ")[-1]
                if _is_number(ver):
                    classifiers_versions.add(float(ver))
        support_versions = [
            version for version in support_versions if
            float(version[:3]) in classifiers_versions
        ]
    results["python_version"] = list({float(version[:3]) for version in support_versions})

    return results


@deco.synchronized
def find_python_versions_by_library_versions(name2version, update_step=30):
    """
    And we add this for the function which calls the concurrent function
    :param update_step:
    :param name2version:
    :return:
    """
    results = defaultdict(dict)
    for ln, lv in name2version.items():
        results[ln] = find_python_version_by_library_version(ln, lv, update_step)
    return dict(results)


def get_requirements_library(path):
    """
    Get all the dependent libraries in the specified requirements.txt
    :param path:
    :return:
    """
    requirements_dict = {}
    with open(path, "r", encoding="utf-8") as f:
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

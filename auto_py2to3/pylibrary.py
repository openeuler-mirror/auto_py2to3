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

import os
import re
import sys
import time
import json
import deco
import requests
import prettytable as pt
from collections import Counter
from collections import defaultdict
from datetime import datetime
from utils import (format_date_en2standard,
                   is_number,
                   find_files,
                   print)

__all__ = ["libraries_detect_and_recommend"]


def _version_str2tuple(vs):
    """

    :param vs:
    :return:
    """
    info = vs.split(".")
    if len(info) == 1 and is_number(info[0]):
        return info[0], "0", "*"
    elif len(info) == 2 and all([
        is_number(info[0]),
        is_number(info[1])
    ]):
        return info[0], info[1], "*"
    elif len(info) == 3 and all([
        is_number(info[0]),
        is_number(info[1]),
        is_number(info[2])
    ]):
        return tuple(info)
    elif len(info) == 3 and all([
        is_number(info[0]),
        is_number(info[1]),
        info[2] == "*"
    ]):
        return info[0], info[1], "*"
    else:
        raise ValueError()


def _update_python_versions():
    """
    Python release date configuration
    :return:
    """
    response = requests.get(url="https://www.python.org/doc/versions/").text
    match_response = re.findall("Python (.*?)</a>, documentation released on (.*?)</li>", response)
    versions = {
        "timestamp": time.time(),
        "versions": dict(
            [(_, format_date_en2standard(en_date, "%d %B %Y")) if en_date[-1].isdigit() else (
                _, format_date_en2standard(en_date[:-1], "%d %B %Y")) for _, en_date in
             match_response]
        )
    }
    with open("conf/python_versions.json", "w", encoding="utf-8") as f:
        json.dump(versions, f, ensure_ascii=False)
    return versions


def get_requirements_library(path):
    """
    Get all the dependent libraries in the specified requirements.txt
    :param path:
    :return:
    """
    requirements_dict = {}
    for requirement_file in find_files(path=path, pattern="*requirements*.txt"):
        with open(requirement_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                if "==" not in line:
                    requirements_dict[line] = ""
                else:
                    ln, lv = line.split("==", 1)
                    requirements_dict[ln] = lv
    return requirements_dict


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
    response = requests.get(url="https://pypi.org/pypi/{0}/json".format(ln)).json()
    newest_library_version = response.get("info", {}).get("version", "")
    results["newest_version"] = newest_library_version
    if not lv:
        print("Python dependency library ({0}) does not have version.".format(ln))
        return results
    # Get the timeline of Python release version
    if not os.path.exists("conf/python_versions.json"):
        # Determine whether there is a timetable cache for the Python release version
        versions = _update_python_versions()["versions"]
    else:
        with open("conf/python_versions.json", "r", encoding="utf-8") as f:
            versions_dict = json.load(f)
        if (datetime.utcfromtimestamp(
            time.time()
        ) - datetime.utcfromtimestamp(
            versions_dict["timestamp"])
        ).days > update_step:
            versions = _update_python_versions()["versions"]
        else:
            versions = versions_dict["versions"]

    # Calculate the exact release time of the dependent library version
    library_version_times = [
        format_date_en2standard(
            item["upload_time_iso_8601"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ) for item in response.get("releases", {}).get(lv, [])
    ]
    if not library_version_times:
        print("Python dependency library ({0}) does not have version({1}).".format(ln, lv))
        return results
    extract_library_version_time = format_date_en2standard(
        Counter(library_version_times).most_common(1)[0][0],
        "%Y-%m-%d",
        return_type="timeObject"
    )
    # Screening strategy:
    # 1. Time filtering according to the time of the library release version and
    # the time of the Python release version
    support_versions = [version for version, _ in filter(
        lambda x: x[1] > 0,
        [(_, (extract_library_version_time - format_date_en2standard(
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
                    version[:3] != "{0}.{1}".format(major, minor)
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    version != "{0}.{1}.{2}".format(major, minor, micro[0])
                ]
        elif option[:2] == ">=":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) >= float("{0}.{1}".format(major, minor))
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) >= int("{0}.{1}.{2}".format(major, minor, micro[0]))
                ]
        elif option[:2] == "<=":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) <= float("{0}.{1}".format(major, minor))
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) <= int("{0}.{1}.{2}".format(major, minor, micro[0]))
                ]
        elif option[:2] == "==":
            major, minor, micro = _version_str2tuple(vs=option[2:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    version[:3] == "{0}.{1}".format(major, minor)
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    version == "{0}.{1}.{2}".format(major, minor, micro[0])
                ]
        elif option[0] == ">" and option[1].isdigit():
            major, minor, micro = _version_str2tuple(vs=option[1:])
            if not micro or micro[0] == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) > float("{0}.{1}".format(major, minor))
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) > int("{0}.{1}.{2}".format(major, minor, micro[0]))
                ]
        elif option[0] == "<" and option[1].isdigit():
            major, minor, micro = _version_str2tuple(vs=option[1:])
            if micro == "*":
                support_versions = [
                    version for version in support_versions if
                    float(version[:3]) < float("{0}.{1}".format(major, minor))
                ]
            else:
                support_versions = [
                    version for version in support_versions if
                    int(version.replace(".", "")) < int("{0}.{1}.{2}".format(major, minor, micro[0]))
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
            url="https://pypi.org/pypi/{0}/{1}/json".format(ln, lv)
        ).json().get("info", {}).get("classifiers", []):
            if "Python :: " in item:
                ver = item.split(" :: ")[-1]
                if is_number(ver):
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


def libraries_detect_and_recommend(target_path):
    """

    :param target_path:
    :return:
    """
    print(">>> Current Python Version: {0}.".format(sys.version))
    detect_recommend_results = pt.PrettyTable(["No", "Library", "Version", "Support Status", "Recommend Version"])
    python_version = float("{0}.{1}".format(sys.version_info.major, sys.version_info.minor))
    print(">>> Statistical analysis of dependent libraries to adapt to the current Python version: Loading...")
    try:
        requirements_libraries = get_requirements_library(
            path=target_path
        )
        python_versions_libraries = find_python_versions_by_library_versions(
            name2version=requirements_libraries
        )
        for i, (ln, versions) in enumerate(python_versions_libraries.items()):
            if python_version in versions["python_version"]:
                detect_recommend_results.add_row(
                    [str(i + 1), ln, versions["version"], "√", versions["version"]]
                )
            else:
                detect_recommend_results.add_row(
                    [str(i + 1), ln, versions["version"], "×", versions["newest_version"]]
                )
    except Exception as e:
        raise e
    print(detect_recommend_results)
    return True

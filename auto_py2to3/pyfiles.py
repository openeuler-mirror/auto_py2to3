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

from .utils import find_files, print
from difflib import HtmlDiff
import os

__all__ = ["files_transform", "bak_files_clear", "html_diff_generate"]

OS_ERROR_CODE = {
    1: "Operation not permitted",
    2: "No such file or directory",
    3: "No such process",
    4: "Interrupted system call",
    5: "Input/output error",
    6: "No such device or address",
    7: "Argument list too long",
    8: "Exec format error",
    9: "Bad file descriptor",
    10: "No child processes",
    11: "Resource temporarily unavailable",
    12: "Cannot allocate memory",
    13: "Permission denied",
    14: "Bad address",
    15: "Block device required",
    16: "Device or resource busy",
    17: "File exists",
    18: "Invalid cross-device link",
    19: "No such device",
    20: "Not a directory",
    21: "Is a directory",
    22: "Invalid argument",
    23: "Too many open files in system",
    24: "Too many open files",
    25: "Inappropriate ioctl for device",
    26: "Text file busy",
    27: "File too large",
    28: "No space left on device",
    29: "Illegal seek",
    30: "Read-only file system",
    31: "Too many links",
    32: "Broken pipe",
    33: "Numerical argument out of domain",
    34: "Numerical result out of range",
    35: "Resource deadlock avoided",
    36: "File name too long",
    37: "No locks available",
    38: "Function not implemented",
    39: "Directory not empty",
    40: "Too many levels of symbolic links",
    42: "No message of desired type",
    43: "Identifier removed",
    44: "Channel number out of range",
    45: "Level 2 not synchronized",
    46: "Level 3 halted",
    47: "Level 3 reset",
    48: "Link number out of range",
    49: "Protocol driver not attached",
    50: "No CSI structure available",
    51: "Level 2 halted",
    52: "Invalid exchange",
    53: "Invalid request descriptor",
    54: "Exchange full",
    55: "No anode",
    56: "Invalid request code",
    57: "Invalid slot",
    59: "Bad font file format",
    60: "Device not a stream",
    61: "No data available",
    62: "Timer expired",
    63: "Out of streams resources",
    64: "Machine is not on the network",
    65: "Package not installed",
    66: "Object is remote",
    67: "Link has been severed",
    68: "Advertise error",
    69: "Srmount error",
    70: "Communication error on send",
    71: "Protocol error",
    72: "Multihop attempted",
    73: "RFS specific error",
    74: "Bad message",
    75: "Value too large for defined data type",
    76: "Name not unique on network",
    77: "File descriptor in bad state",
    78: "Remote address changed",
    79: "Can not access a needed shared library",
    80: "Accessing a corrupted shared library",
    81: ".lib section in a.out corrupted",
    82: "Attempting to link in too many shared libraries",
    83: "Cannot exec a shared library directly",
    84: "Invalid or incomplete multibyte or wide character",
    85: "Interrupted system call should be restarted",
    86: "Streams pipe error",
    87: "Too many users",
    88: "Socket operation on non-socket",
    89: "Destination address required",
    90: "Message too long",
    91: "Protocol wrong type for socket",
    92: "Protocol not available",
    93: "Protocol not supported",
    94: "Socket type not supported",
    95: "Operation not supported",
    96: "Protocol family not supported",
    97: "Address family not supported by protocol",
    98: "Address already in use",
    99: "Cannot assign requested address",
    100: "Network is down",
    101: "Network is unreachable",
    102: "Network dropped connection on reset",
    103: "Software caused connection abort",
    104: "Connection reset by peer",
    105: "No buffer space available",
    106: "Transport endpoint is already connected",
    107: "Transport endpoint is not connected",
    108: "Cannot send after transport endpoint shutdown",
    109: "Too many references: cannot splice",
    110: "Connection timed out",
    111: "Connection refused",
    112: "Host is down",
    113: "No route to host",
    114: "Operation already in progress",
    115: "Operation now in progress",
    116: "Stale NFS file handle",
    117: "Structure needs cleaning",
    118: "Not a XENIX named type file",
    119: "No XENIX semaphores available",
    120: "Is a named type file",
    121: "Remote I/O error",
    122: "Disk quota exceeded",
    123: "No medium found",
    124: "Wrong medium type",
    125: "Operation canceled",
    126: "Required key not available",
    127: "Key has expired",
    128: "Key has been revoked",
    129: "Key was rejected by service",
    130: "Owner died",
    131: "State not recoverable"
}


def files_transform(target_path,
                    interpreter_command_name):
    """
    Provide the specific implementation method of Python2 to Python3 function
    for searching all the specified .py files of the project,
    use the 2to3.py module for advanced packaging,
    and print detailed possible causes of errors.

    :param target_path:
           str, project path
    :param interpreter_command_name:
           str, interpreter command name
    :return: bool, ignore
    """
    for file in find_files(path=target_path, pattern="*.py"):
        try:
            os_code = os.system("{0} {1} -w {2}".format(
                interpreter_command_name,
                os.path.dirname(os.path.abspath(__file__)) + "/2to3.py",
                file)
            )
            if os_code != 0:
                print(">>> ERROR: " + OS_ERROR_CODE.get(os_code, 1))
        except Exception as e:
            raise e
    print(">>> *.py files had been 2to3 transformed!")
    return True


def bak_files_clear(target_path):
    """
    Provide code deletion function for Python2 backup.

    :param target_path:
           str, project path
    :return: bool, ignore
    """
    for file in find_files(path=target_path, pattern="*.bak"):
        try:
            os.remove(file)
        except Exception as e:
            raise e
    print(">>> *.bak files had been removed!")
    return True


def html_diff_generate(target_path):
    """
    Generate converted comparison file (. HTML)

    :param target_path: str, project path
    :return: bool, ignore
    """
    htmlDiff = HtmlDiff()
    for file in find_files(path=target_path, pattern="*.py"):
        print(file)
        try:
            with open(file, "r", encoding='utf-8') as f:
                advanced = [line.strip('\n') for line in f.readlines()]
            with open(file + ".bak", "r", encoding='utf-8') as f:
                origin = [line.strip('\n') for line in f.readlines()]

            out_path = os.path.join(target_path, file.split("/")[-1].split(".")[0] + "_diff_comp.html")
            with open(out_path, 'w', encoding="utf-8") as f:
                f.writelines(htmlDiff.make_file(origin, advanced))
        except Exception as e:
            raise e
    print(">>> *_diff_comp.html files had been generated!")
    return True

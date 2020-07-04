# -*- coding: utf-8 -*-

"""Main module."""
import os

transfer_abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/tests/"

for each_name in [p for p in os.listdir(transfer_abs_path) if os.path.splitext(p)[1] == ".py"]:
    r_v = os.system("python libs/2to3-script.py -wn {0}".format(transfer_abs_path + each_name))
    print(r_v)

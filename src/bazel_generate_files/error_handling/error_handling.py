#!/usr/bin/python3

import sys
import os
import re
from .check_variables import check_variables

#Check that the file have 6 lines

def check_nbr_line(bazel_env):
    try:
        if (len(bazel_env) < 6):
            raise NameError("Missing lines in bazel.env file.")
        elif (len(bazel_env) > 6):
            raise NameError("Too many lines in bazel.env file.")
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_bazel_file(bazel_env):
    check_nbr_line(bazel_env)
    check_variables(bazel_env)

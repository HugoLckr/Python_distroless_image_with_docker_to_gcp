#!/usr/bin/python3

import sys
from error_handling.error_handling import check_bazel_file
from get_bazel_file import get_bazel_file
from generate_files import generate_files
from shutil import copyfile

def main():
    bazel_env = get_bazel_file()      #get bazel env
    check_bazel_file(bazel_env)       #error handling
    generate_files(bazel_env)         #generating

if __name__ == "__main__":
    main()
#!/usr/bin/python3

from glob import glob
import sys

def get_path_bazel_file():
    try:
        path = glob('../*/*/bazel.env')          #search were is the bazel file
        if (len(path) == 1) :
            return str(path[0])
        else:
            raise NameError("bazel.env file doesn't found.")
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def get_bazel_file():
    try:
        path = get_path_bazel_file()
        f=open(path, "r")
        lines = f.readlines()
        bazel_env=[]
        for line in lines:
            bazel_env.append(line)
        f.close()
        return bazel_env
    except NameError:
        print("Error: Can't open ", path, ".")
        sys.exit(84)
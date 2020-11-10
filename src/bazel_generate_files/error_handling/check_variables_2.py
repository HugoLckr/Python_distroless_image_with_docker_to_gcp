#!/usr/bin/python3

import sys
import os
import re
##
##For every variable, check that file/directory exist, or the syntax
##
def get_repository_name(bazel_env):
    try:
        for line in bazel_env:
            variables=line.split("=")
            if (variables[0] == "repository_name"):
                check_repository_name(variables[0], variables[1])
                repository_name = variables[1]
                repository_name = repository_name[:-1] if (repository_name[-1:] == '\n') else repository_name
                return repository_name
        raise NameError("repository_name doesn't exist.")
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def get_path_pythons_files(bazel_env):
    try:
        for line in bazel_env:
            variables=line.split("=")
            if (variables[0] == "path_to_pythons_files"):
                check_path_pythons_files(variables[0], variables[1], bazel_env)
                path_python_files = variables[1]
                path_python_files = path_python_files[:-1] if (path_python_files[-1:] == '\n') else path_python_files
                return path_python_files
        raise NameError("path python's files.")
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_repository_name(variable_name, variable):
    try:
        variable = variable[:-1] if (variable[-1:] == '\n') else variable
        if (not os.path.isdir("../connector_image/"+variable+"/")):
            raise NameError("Can't found ../connector_image/"+variable+"/")
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_image_tag(variable_name, variable):
    try:
        
        variable = variable[:-1] if (variable[-1:] == '\n') else variable
        if (len(variable) > 128):
            raise NameError("Tag too long, max lenght = 128 characters")
        elif (len(variable) > 0):
            regex=r"^([0-9]|[a-z])*[a-z-A-Z0-9\.\-]*([0-9]|[a-z])$"
            if (not re.match(regex, variable)):
                raise NameError("Tag formating:"+variable)
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_path_env_file(variable_name, variable, bazel_env):
    try:
        repository_name=get_repository_name(bazel_env)
        variable = variable[:-1] if (variable[-1:] == '\n') else variable
        variable = variable[1:] if (variable[0] == '/') else variable
        if (not os.path.isfile("../connector_image/"+repository_name+"/"+variable)):
            raise NameError("Can't found env file: ../connector_image/"+repository_name+"/"+variable)
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_path_pythons_files(variable_name, variable, bazel_env):
    try:
        repository_name=get_repository_name(bazel_env)
        variable = variable[:-1] if (variable[-1:] == '\n') else variable
        variable = variable[1:] if (variable[0] == '/') else variable
        if (not os.path.isdir("../connector_image/"+repository_name+"/"+variable)):
            raise NameError("Can't found python's files: ../connector_image/"+repository_name+"/"+variable)
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_main_file(variable_name, variable, bazel_env):
    try:
        repository_name=get_repository_name(bazel_env)
        path_pythons_files=get_path_pythons_files(bazel_env)
        variable = variable[:-1] if (variable[-1:] == '\n') else variable
        if (not os.path.isfile("../connector_image/"+repository_name+"/"+path_pythons_files+"/"+variable)):
            raise NameError("Can't found python's files main: ../connector_image/"+repository_name+"/"+variable)
    except NameError as e:
        print("Error:", e)
        sys.exit(84)

def check_path_requirements(variable_name, variable, bazel_env):
    try:
        repository_name=get_repository_name(bazel_env)
        variable = variable[:-1] if (variable[-1:] == '\n') else variable
        variable = variable[1:] if (variable[0] == '/') else variable
        if (not os.path.isfile("../connector_image/"+repository_name+"/"+variable)):
            raise NameError("Can't found requirement's file: ../connector_image/"+repository_name+"/"+variable)
    except NameError as e:
        print("Error:", e)
        sys.exit(84)
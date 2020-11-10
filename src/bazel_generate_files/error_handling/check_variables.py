#!/usr/bin/python3

import sys
from .check_variables_2 import check_repository_name, check_image_tag, check_path_env_file, \
                                check_path_pythons_files, check_main_file, check_path_requirements

def check_variable(variable_name, variable, bazel_env):
    if (variable_name == "repository_name"):
        check_repository_name(variable_name, variable)
    elif (variable_name == "image_tag"):
        check_image_tag(variable_name, variable)
    elif (variable_name == "path_to_env_file"):
        check_path_env_file(variable_name, variable, bazel_env)
    elif (variable_name == "path_to_pythons_files"):
        check_path_pythons_files(variable_name, variable, bazel_env)
    elif (variable_name == "python_main"):
        check_main_file(variable_name, variable, bazel_env)
    elif (variable_name == "path_to_requirements.txt"):
        check_path_requirements(variable_name, variable, bazel_env)

def check_line(array_line, bazel_env):
    try:
        checked = 0
        names_lines=["repository_name", "image_tag", "path_to_env_file", 
                    "path_to_pythons_files", "python_main", "path_to_requirements.txt"]
        for i in names_lines:
            if (i == array_line[0]):
                checked = 1
                check_variable(array_line[0], array_line[1], bazel_env)
        if (checked != 1):
            raise NameError("Variable '"+array_line[0]+
                            "'. Variables accepted are: "+
                            names_lines[0]+" / "+names_lines[1]
                            +" / "+names_lines[2]+" / "+names_lines[3]+" / "+
                            names_lines[4]+" / "+names_lines[5])
    except NameError as e:
        print("Error :", e)
        sys.exit(84)

def check_variables(bazel_env):
    try:
        for line in bazel_env:
            array_line = line.split("=")
            if (len(array_line) != 2):             #check that the format its (name=var)
                raise NameError("Error Formating :")
            check_line(array_line, bazel_env)      #check every line one by one
    except NameError as e:
        print(e, line, end="")
        sys.exit(84)
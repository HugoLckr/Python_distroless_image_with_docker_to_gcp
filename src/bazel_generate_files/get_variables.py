#!/usr/bin/python3

import sys

#Put in variables the informations read before in bazel env file

def get_repository_name(bazel_env):
    for line in bazel_env:
        variables=line.split("=")
        if (variables[0] == "repository_name"):
            repository_name = variables[1]
            repository_name = repository_name[:-1] if (repository_name[-1:] == '\n') else repository_name
            return repository_name

def get_image_tag(bazel_env):
    for line in bazel_env:
        variables=line.split("=")
        if (variables[0] == "image_tag"):
            tag = variables[1]
            if (len(tag) == 0 or (len(tag) == 1 and tag[0] == '\n')):
                tag = "latest"
            tag = tag[:-1] if (tag[-1:] == '\n') else tag      
            return tag

def get_path_to_env_file(bazel_env, repository_name):
    for line in bazel_env:
        variables=line.split("=")
        if (variables[0] == "path_to_env_file"):
            path_to_env = variables[1]
            path_to_env = path_to_env[:-1] if (path_to_env[-1:] == '\n') else path_to_env      
            return path_to_env

def get_path_to_pythons_files(bazel_env, repository_name):
    for line in bazel_env:
        variables=line.split("=")
        if (variables[0] == "path_to_pythons_files"):
            path_python_files = variables[1]
            path_python_files = path_python_files[:-1] if (path_python_files[-1:] == '\n') else path_python_files   
            return path_python_files
    
def get_python_main(bazel_env):
    for line in bazel_env:
        variables=line.split("=")
        if (variables[0] == "python_main"):
            python_main = variables[1]
            python_main = python_main[:-1] if (python_main[-1:] == '\n') else python_main
            return python_main

def get_path_to_requirement(bazel_env, repository_name):
    for line in bazel_env:
        variables=line.split("=")
        if (variables[0] == "path_to_requirements.txt"):
            path_req = variables[1]
            path_req = path_req[:-1] if (path_req[-1:] == '\n') else path_req
            return path_req
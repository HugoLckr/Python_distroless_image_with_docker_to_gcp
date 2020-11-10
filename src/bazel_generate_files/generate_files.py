#!/usr/bin/python3

import sys
import fileinput
import os
from shutil import copyfile
from get_variables import *
import stat

#Generate every files one by one from a template or by modifying the existant one.

def generate_workspace(path_to_requirement, repository_name):
    f=open("generated/WORKSPACE","w+")
    new_line = '   requirements = \"//'+repository_name+':'+path_to_requirement+'\",'
    template = "templates/WORKSPACE_template"
    macs = {
        '   requirements = "//$[REPLACE]$",': new_line
    }
    for line in fileinput.input(template):
        line = line.rstrip('\r\n')
        f.write(macs.get(line, line)+"\n")
    f.close()
    copyfile("generated/WORKSPACE", "../connector_image/WORKSPACE")

def generate_docker_compose(repository_name, image_tag, path_to_env_file):
    f=open("generated/docker-compose.yml","w+")
    new_line_image = '    image: bazel/'+repository_name+':'+image_tag
    new_line_env = '    env_file: ./'+repository_name+'/'+path_to_env_file
    template = "templates/docker-compose.yml_template"
    macs = {
        '    image: bazel/$[REPLACE]$' : new_line_image,
        '    env_file: ./$[REPLACE]$': new_line_env
    }
    for line in fileinput.input(template):
        line = line.rstrip('\r\n')
        f.write(macs.get(line, line)+"\n")
    f.close()
    copyfile("generated/docker-compose.yml", "../connector_image/docker-compose.yml")

def generate_run(repository_name, image_tag):
    f=open("generated/run","w+")
    new_line = 'bazel run //'+repository_name+':'+image_tag
    template = "templates/run_template"
    macs = {
        'bazel run //$[REPLACE]$': new_line
    }
    for line in fileinput.input(template):
        line = line.rstrip('\r\n')
        f.write(macs.get(line, line)+"\n")
    f.close()
    copyfile("generated/run", "../connector_image/run")
    st = os.stat('../connector_image/run')
    os.chmod("../connector_image/run", st.st_mode | stat.S_IEXEC)

def get_new_path_to_requirement(older_path_to_requirement, new_path):
    divised_path = older_path_to_requirement.split('/')
    divised_path = divised_path[:-1]
    divised_path.append(new_path)
    new_path_to_requirement=""
    for i in divised_path:
        new_path_to_requirement += i+'/'
    new_path_to_requirement = new_path_to_requirement[:-1]
    new_path_to_requirement = new_path_to_requirement[:-1] if (new_path_to_requirement[-1:] == '\n') else new_path_to_requirement
    return new_path_to_requirement

def modify_requirement(path_to_requirement, repository_name):
    complete_path='../connector_image/'+repository_name+'/'+path_to_requirement
    older_file=open(complete_path, "r")
    file_name=path_to_requirement.split("/")
    new_file=open("generated/"+file_name[-1],"w")
    lines = older_file.readlines()
    for line in lines:
        divised_line = line.split(" ")
        if (len(divised_line) == 2):
            if (divised_line[0] == '-r'):
                modify_requirement(get_new_path_to_requirement(path_to_requirement, divised_line[1]) ,repository_name)
        divised_line = line.split("==")
        new_file.write(divised_line[0]+'\n') if (len(divised_line) == 2) else new_file.write(line)
    new_file.close()
    older_file.close()
    copyfile("generated/"+file_name[-1], complete_path)

def get_older_line(complete_path):
    f=open(complete_path,"r")
    lines = f.readlines()
    for line in lines:
        line_divised=line.split("=")
        if (line_divised[0] == "PROJECT_ROOT"):
            older_line=line
    f.close()
    return older_line

def modify_env(path_to_env_file, repository_name, path_to_python_files, python_main):
    complete_path='../connector_image/'+repository_name+'/'+path_to_env_file
    older_line = get_older_line(complete_path)
    f=open("generated/env","w")
    if (python_main[-3:] == '.py'):
        python_main = python_main[:-3]
    new_line = 'PROJECT_ROOT=/app/'+repository_name+'/'+path_to_python_files+'/'+python_main+'.binary.runfiles/__main__/'+repository_name+'/'+path_to_python_files+'/'
    macs = {
        older_line: new_line
    }
    for line in fileinput.input(complete_path):
        line = line.rstrip('\r\n')
        f.write(macs.get(line, line)+"\n")
    f.close()
    os.remove(complete_path)
    copyfile("generated/env", complete_path)

def get_req_git(line):
    line = line.split("git+https://bitbucket.org/worldsensing_traffic/")
    line = line[1].split(".")
    if (line[0][-4:] == '_lib'):
        line[0] = line[0][:-4]
    return line[0]

def get_all_requirements_names(path_to_requirement, repository_name):
    complete_path='../connector_image/'+repository_name+'/'+path_to_requirement
    older_file=open(complete_path, "r")
    lines = older_file.readlines()
    all_requirements_names = []
    for line in lines:
        divised_line = line.split(" ")    #
        if (len(divised_line) == 2):      #For "-r file.txt"
            if (divised_line[0] == '-r'): #
                all_requirements_names += get_all_requirements_names(get_new_path_to_requirement(path_to_requirement, divised_line[1]) ,repository_name)
        else :
            divised_line = line.split("==")                                                                   #
            divised_line[0] = divised_line[0][:-1] if (divised_line[0][-1:] == '\n') else divised_line[0]     #For lib==1.1.1
            if (divised_line[0][:2] != "--" and divised_line[0][:4] != 'git+' and len(divised_line[0]) > 0) : #
                all_requirements_names.append(divised_line[0])
            elif (divised_line[0][:4] == 'git+'):                             #For git+http....
                all_requirements_names.append(get_req_git(divised_line[0]))
    older_file.close()
    return all_requirements_names

def generate_build(repository_name, path_to_python_files, python_main, path_to_requirement, image_tag):
    f=open("generated/BUILD","w+")
    template = "templates/BUILD_template"
    python_main_without_py = python_main[:-3] if (python_main[-3:] == '.py') else python_main
    requirements_list=get_all_requirements_names(path_to_requirement, repository_name)
    requirements_lines = ""
    for req in requirements_list:
        requirements_lines += '        requirement("'+req+'"),\n'
    requirements_lines = requirements_lines[:-1]
    macs = {
        '        $[ADD_REQUIREMENTS]$': requirements_lines,
        '    name = "$[py_image_name]$",' : '    name = "'+path_to_python_files+'/'+python_main_without_py+'",',
        '    srcs = glob($["py_src/*.py"]$),' : '    srcs = glob(["'+path_to_python_files+'/*.py"]),',
        '    main = "$[py_main]$",' : '    main = "'+python_main+'",',
        '    data = glob($["py_src/**"]$),' : '    data = glob(["'+path_to_python_files+'/**"]),',
        '    name = "$[container_image_name]$",' : '    name = "'+image_tag+'",',
        '    base = "$[base_name]$",' : '    base = "'+path_to_python_files+'/'+python_main_without_py+'",',
    }
    for line in fileinput.input(template):
        line = line.rstrip('\r\n')
        f.write(macs.get(line, line)+"\n")
    f.close()
    copyfile("generated/BUILD", "../connector_image/"+repository_name+"/BUILD")

def generate_files(bazel_env):
    #Get variables
    repository_name=get_repository_name(bazel_env)
    image_tag=get_image_tag(bazel_env)
    path_to_env_file=get_path_to_env_file(bazel_env, repository_name)
    path_to_python_files=get_path_to_pythons_files(bazel_env, repository_name)
    python_main=get_python_main(bazel_env)
    path_to_requirement=get_path_to_requirement(bazel_env, repository_name)
    #Generate, modify files
    generate_workspace(path_to_requirement, repository_name)
    generate_docker_compose(repository_name, image_tag, path_to_env_file)
    generate_run(repository_name, image_tag)
    modify_requirement(path_to_requirement, repository_name)
    modify_env(path_to_env_file, repository_name, path_to_python_files, python_main)
    generate_build(repository_name, path_to_python_files, python_main, path_to_requirement, image_tag)
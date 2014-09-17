#!/usr/bin/python

glint_lib_directory='/var/lib/glint'
horizon_git_repo='https://github.com/rd37/horizon'
glint_git_repo='https://github.com/hep-gc/glint.git'

import sys,subprocess

from glint_arg_parser import GlintArgumentParser

def proceed(msg):
    print msg
    input = raw_input()
    if input == '' or input == 'y' or input == 'Y':
       return True
    return False

def execute_command(cmd_args):
    process = subprocess.Popen(cmd_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = process.communicate()
    if err:
        print "warning: %s"%err
    return out,err

def check_dependencies():
    print "dependency check: check if git and user glint exist"
    [out,err] = execute_command(['which','git'])
    if "no git" in out:
        print "Error, unable to find git tool, please install and attempt glint install again"
        return False
    [out,err] = execute_command(['grep','glint','/etc/passwd'])
    if out == '':
        print "Warning, unable to find system user glint"
        if proceed('Do you wish to setup glint as a User? [Y,n]'):
            print "Ok lets setup glint user "
            [out,err] = execute_command(['python','glint_system_create_user.py','create-glint-user'])
            if err:
                print "Unable to create glint user"
                return False
            #print "out: %s"%out
            return True
        else:    
            return False

    return True 

def download_horizon():
    print "download horizon using git clone"
    [out,err] = execute_command(['git','clone','%s'%horizon_git_repo,'%s/horizon'%glint_lib_directory])
    if err:
        print "Unable to git clone glint-horizon "
        return False
    print "git clone glint-horizon result %s"%out
    return True

def download_glint():
    print "download glint using git clone"
    [out,err] = execute_command(['git','clone','%s'%glint_git_repo,'%s/glint'%glint_lib_directory])
    if err:
        print "Unable to git clone glint"
        return False
    print "git clone glint result %s"%out
    return True


def install_horizon():
    print "install glint-horizon"

def install_glint():
    print "install glint"

def uninstall_horizon():
    print "uninstall glint-horizon"

def uninstall_glint():
    print "uninstall glint"

########### Uninstalling glint and and glint-horizon
def remove_glint():
    print "Try Removing Glint Git Repository"
    [out,err] = execute_command(['rm','-rf','/var/lib/glint/glint'])

def remove_glint_horizon():
    print "Try Removing Glint-Horizon Git Repository"
    [out,err] = execute_command(['rm','-rf','/var/lib/glint/horizon'])
    
########### Main Func

gap = GlintArgumentParser()
gap.init_git_arg_parser()
args = gap.parser.parse_args()
print args

if args.install is not None:
    if args.glint_url is not None  and args.glint_hor_url is not None:
        glint_git_repo = args.glint_url
        horizon_git_repo = args.glint_hor_url
        print "Overide default Git Repos with %s and %s"%(glint_git_repo,horizon_git_repo)
    if check_dependencies():
        print "Git and User Glint are OK ... moving along"
        
        if args.install == 'all':
            download_horizon()
            download_glint()
            install_horizon()
            install_glint()
        elif args.install == 'glint':
            download_glint()
            install_glint()
        elif args.install == 'horizon':
            download_horizon()
            install_horizon()
    else:
        print "Check your Setup, system requirements are the git tool and user glint to exist"
elif args.uninstall is not None:
    if args.uninstall == 'all':
        uninstall_horizon()
        uninstall_glint()
        remove_glint()
        remove_glint_horizon()
    elif args.install == 'glint':
        uninstall_glint()
        remove_glint()
    elif args.install == 'horizon':
        uninstall_horizon()
        remove_glint_horizon()

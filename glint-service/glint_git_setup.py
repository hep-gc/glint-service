#!/usr/bin/python

glint_lib_directory='/var/lib/glint'
horizon_git_repo='https://github.com/rd37/horizon.git'
glint_git_repo='https://github.com/hep-gc/glint.git'
glint_inst_type='default'
horizon_inst_type='default'
glint_server='django'
glint_horizon_server='django'

cfg_dir = '/etc/glint'
pkg_dir = 'glint-service'

import sys,subprocess

from glint_arg_parser import GlintArgumentParser

def proceed(msg):
    print msg
    input = raw_input()
    if input == '' or input == 'y' or input == 'Y':
       return True
    return False

def execute_command(cmd_args,input):
    if input is None:
        process = subprocess.Popen(cmd_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = process.communicate()
    else:
        #print "Need to use use input"
        process = subprocess.Popen(cmd_args,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = process.communicate(input=input)
    if err:
        print "warning: %s"%err
    sys.stdout.flush()
    return out,err

def check_dependencies():
    print "dependency check: check if git and user glint exist"
    [out,err] = execute_command(['which','git'],None)
    if "no git" in out:
        print "Error, unable to find git tool, please install and attempt glint install again"
        return False
    [out,err] = execute_command(['grep','glint','/etc/passwd'],None)
    if out == '':
        print "Warning, unable to find system user glint"
        if proceed('Do you wish to setup glint as a User? [Y,n]'):
            print "Ok lets setup glint user "
            [out,err] = execute_command(['python','glint_system_create_user.py','create-glint-user'],None)
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
    [out,err] = execute_command(['git','clone','%s'%horizon_git_repo,'%s/horizon'%glint_lib_directory],None)
    if err:
        print "Unable to git clone glint-horizon "
        return False
    print "git clone glint-horizon result %s"%out
    return True

def download_glint():
    print "download glint using git clone"
    [out,err] = execute_command(['git','clone','%s'%glint_git_repo,'%s/glint'%glint_lib_directory],None)
    if err:
        print "Unable to git clone glint"
        return False
    print "git clone glint result %s"%out
    return True


def install_horizon():
    print "Install glint-horizon"
    print "Install library pre-reqs"
    [out,err] = execute_command(['yum','install','libxml2-devel'],'y')
    print out
    [out,err] = execute_command(['yum','install','libxslt-devel'],'y')
    print out
    [out,err] = execute_command(['yum','install','gcc'],'y')
    print out
    [out,err] = execute_command(['yum','install','git-core'],'y')
    print out
    [out,err] = execute_command(['yum','install','python-virtualenv'],'y')
    print out
    [out,err] = execute_command(['yum','install','python-devel'],'y')
    print out
    [out,err] = execute_command(['yum','install','openssl-devel'],'y')
    print out
    [out,err] = execute_command(['yum','install','libffi-devel'],'y')
    print out
    if horizon_inst_type == 'default':
        print "Install Horizon using default (virtualenv in /var/lib/glint/horizon/.venv)"
        [out,err] = execute_command(['python','/var/lib/glint/horizon/tools/install_venv.py'],None)
        [out,err] = execute_command(['chown','-R','glint','/var/lib/glint/horizon'],None)
        [out,err] = execute_command(['chgrp','-R','glint','/var/lib/glint/horizon'],None)
    elif horizon_inst_type == 'replace':
        print "Currently Unsupported: Remove openstack-horizon and replace with glint-horizon"
    elif horizon_inst_type == 'contextualize':
        print "Currently Unsupported: Insert or Replace parts of the openstack-horizon installation"
    else:
        print "Unrecognized installation type for glint - %s - error exiting"%horizon_inst_type
        return
    print "IP:Open Port used for glint-horizon ... port 8080, restart networking"
    
    print "mkdir /var/run/glint and change permissions"
    [out,err] = execute_command(['mkdir','/var/run/glint'],None)
    [out,err] = execute_command(['chown','glint','/var/run/glint'],None)
    [out,err] = execute_command(['chgrp','glint','/var/run/glint'],None)

    if glint_horizon_server == 'django':
        print "Setup /usr/bin/glint-horizon as main system start application (reads cfg file for gl-hor location)"
        #copy glint-horizon from /var/lib/glint/horizon to /usr/bin/glint-horizon
        [out,err] = execute_command(['cp','%s/glint-horizon'%pkg_dir,'/usr/bin/.'],None)
        [out,err] = execute_command(['chmod','755','/usr/bin/glint-horizon'],None)
        print "Setup /etc/init.d/glint-horizon as a service"
        [out,err] = execute_command(['cp','%s/openstack-glint-horizon'%pkg_dir,'/etc/init.d/.'],None)
        [out,err] = execute_command(['chmod','755','/etc/init.d/openstack-glint-horizon'],None)
    elif glint_horizon_server == 'apache':
        print "Currently Unsupprted: Register glint-horizon with local apache this is used by /user/bin/glint-horizon to start stop the apache app"
        print "Currently Unsupported: Setup /usr/bin/glint-horizon as main system start application (reads cfg file for gl-hor location)"
        print "Currently Unsupported: Setup /etc/init.d/glint-horizon as a service"

def install_glint():
    print "Install glint"
    if glint_inst_type == 'default':
        print "Leave glint in /var/lib/glint/glint, but change own and group to glint"
        [out,err] = execute_command(['chown','-R','glint','/var/lib/glint/glint'],None)
        [out,err] = execute_command(['chgrp','-R','glint','/var/lib/glint/glint'],None)
    elif glint_inst_type == 'local':
        print "Currently Unsupported: Install glint into sites-packages - use setup.py"
    else:
        print "Unrecognized installation type for glint - %s - error exiting"%glint_inst_type
        return
    print "IP:Open Glint Port 9494 and restart networking"
     
    print "mkdir /var/run/glint and change permissions"
    [out,err] = execute_command(['mkdir','/var/log/glint-service'],None)
    [out,err] = execute_command(['chown','glint','/var/log/glint-service'],None)
    [out,err] = execute_command(['chgrp','glint','/var/log/glint-service'],None)
    
    print "copy glint service yaml conf file"
    [out,err] = execute_command(['cp','%s/glint_services.yaml'%cfg_dir,'/var/lib/glint/glint/.'],None)
    [out,err] = execute_command(['chown','glint:glint','/var/lib/glint/glint/glint_services.yaml'],None)
    
    if glint_server == 'django':
        print "Setup /usr/bin/glint as main start of glint server from installed (either /var/lib or site-packeges) using django test server"
        [out,err] = execute_command(['cp','%s/glint'%pkg_dir,'/usr/bin/.'],None)
        [out,err] = execute_command(['chmod','755','/usr/bin/glint'],None)
        print "Setup /etc/init.d/glint as a service "
        [out,err] = execute_command(['cp','%s/openstack-glint'%pkg_dir,'/etc/init.d/.'],None)
        [out,err] = execute_command(['chmod','755','/etc/init.d/openstack-glint'],None)
    elif glint_server == 'paste':
        print "Currently Unsupported: Setup /usr/bin/glint as main start of glint server from installed (either /var/lib or site-packeges) using django test server"
        print "Currently Unsupported: Setup /etc/init.d/glint as a service "

def uninstall_horizon():
    print "Uninstall glint-horizon"
    print "Stop glint-horizon service and remove it"
    [out,err] = execute_command(['rm','/etc/init.d/openstack-glint-horizon'],None)
    print "Remove /usr/bin/glint-horizon script"
    [out,err] = execute_command(['rm','/usr/bin/glint-horizon'],None)
    if glint_horizon_server == 'django':
         print "Nothing to Do for django server"
    elif glint_horizon_server == 'apache':
         print "Currently Unsupported:Remove glint-horizon from apache"
    
    print "IP:Close port used by glint-horizon"
    
    if horizon_inst_type == 'default':
        print "IP: UNInstall Horizon using default (virtualenv in /var/lib/glint/horizon/.venv)"
    elif horizon_inst_type == 'replace':
        print "Currently Unsupported: Remove glint-horizon and replace with openstack-horizon"
    elif horizon_inst_type == 'contextualize':
        print "Currently Unsupported: Revert changes to parts of the openstack-horizon installation"

def uninstall_glint():
    print "uninstall glint"
    if glint_inst_type == 'default':
        print "Default Unistall - nothing to do here"
    elif glint_inst_type == 'local':
        print "Currently Unsupported: remove glint from sites-packages - use setup.py"
    
    print "Remove /etc/init.d/openstack-glint "
    [out,err] = execute_command(['rm','/etc/init.d/openstack-glint'],None)
    print "Remove /usr/bin/glint script"
    [out,err] = execute_command(['rm','/usr/bin/glint'],None)
    print "Remove log directory"
    [out,err] = execute_command(['rm','/var/log/glint-service'],None)

    print "IP: Shutdown Glint Port 9494 and restart networking"

########### Uninstalling glint and and glint-horizon
def remove_glint():
    print "Try Removing Glint Git Repository"
    [out,err] = execute_command(['rm','-rf','/var/lib/glint/glint'],None)

def remove_glint_horizon():
    print "Try Removing Glint-Horizon Git Repository"
    [out,err] = execute_command(['rm','-rf','/var/lib/glint/horizon'],None)
    
########### Main Func

gap = GlintArgumentParser()
gap.init_git_arg_parser()
args = gap.parser.parse_args()
print args

if args.install is not None:
    if args.glint_url is not None:
        glint_git_repo = args.glint_url
    if args.glint_hor_url is not None:
        horizon_git_repo = args.glint_hor_url
    if args.glint_inst_type is not None:
        glint_inst_type = args.glint_inst_type
    if args.hor_inst_type is not None:
        horizon_inst_type = args.hor_inst_type
    if args.glint_server is not None:
        glint_server = args.glint_server[0] 
    if args.glint_horizon_server is not None:
        glint_horizon_server = args.glint_horizon_server[0]
    
    if check_dependencies():
        print "Git and User Glint are OK ... moving along"
        
        if args.install[0] == 'all':
            download_horizon()
            download_glint()
            install_horizon()
            install_glint()
        elif args.install[0] == 'glint':
            download_glint()
            install_glint()
        elif args.install[0] == 'horizon':
            download_horizon()
            install_horizon()
    else:
        print "Check your Setup, system requirements are the git tool and user glint to exist"
elif args.uninstall is not None:
    if args.uninstall[0] == 'all':
        uninstall_horizon()
        uninstall_glint()
        remove_glint()
        remove_glint_horizon()
    elif args.install[0] == 'glint':
        uninstall_glint()
        remove_glint()
    elif args.install[0] == 'horizon':
        uninstall_horizon()
        remove_glint_horizon()

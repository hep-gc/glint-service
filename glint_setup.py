#!/usr/bin/python

import yaml,sys,subprocess,os

glint_url = 'https://github.com/hep-gc/glint.git'
horizon_url = 'https://github.com/rd37/horizon.git'
gl_inst_type = 'default'
hor_inst_type= 'default'
gl_user_id=171
glint_server='django'
glint_horizon_server='django'

def set_env_openstack_admin_pw():
    print "---------------------------"
    print "Enter Openstack Admin Password "
    pw = sys.stdin.readline()
    env_dict={}
    env_dict['OS_PASSWORD']=pw.rstrip()
    os.environ.update(env_dict)

def execute_command(cmd_args):
    process = subprocess.Popen(cmd_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = process.communicate()
    if err:
        print "warning: %s"%err
    return out,err

def create_glint_user():
    print "creating glint user"
    [out,err] = execute_command(['python','glint_system_create_user.py','create-glint-user','%s'%gl_user_id])
    #print out

def download_install_glint():
    print "download install glint"
    [out,err] = execute_command(['python','glint_git_setup.py','-install','all','-glint_url','%s'%glint_url,'-glint_hor_url','%s'%horizon_url,'-glint_inst_type','%s'%gl_inst_type,'-hor_inst_type','%s'%hor_inst_type,'-glint_server','%s'%glint_server,'-glint_horizon_server','%s'%glint_horizon_server])
    print out

def register_glint_in_openstack():
    print "register glint in openstack"
    set_env_openstack_admin_pw()
    [out,err] = execute_command(['python','glint_openstack_registration.py'])
    #print out

def remove_glint_user():
    print "remove glint user"
    [out,err] = execute_command(['python','glint_system_create_user.py','remove-glint-user','%s'%gl_user_id])
    print out

def delete_installed_glint():
    print "delete installed glint"
    [out,err] = execute_command(['python','glint_git_setup.py','-uninstall','all','-glint_inst_type','%s'%gl_inst_type,'-hor_inst_type','%s'%hor_inst_type,'-glint_server','%s'%glint_server,'-glint_horizon_server','%s'%glint_horizon_server])
    print out

def deregister_glint_in_openstack():
    print "deregister glint in openstack"
    set_env_openstack_admin_pw()
    [out,err] = execute_command(['python','glint_openstack_registration.py','uninstall'])
    print out

def show_usage():
    print "Usage"
    print "INSTALL: python glint_setup.py install"
    print "UNINSTALL: python glint_setup.py uninstall"

def start_glint_service():
    print "If all is setup right, this sould start both glint service and glint-horizon dashboard"
    print "Start glint service"
    [out,err] = execute_command(['service','openstack-glint','start'])
    print "Start glint-horizon dashboard"
    [out,err] = execute_command(['service','openstack-glint-horizon','start'])

def stop_glint_service():
    print "Stop glint Service"
    [out,err] = execute_command(['service','openstack-glint','stop'])
    print "Stop glint-horizon dashboard"
    [out,err] = execute_command(['service','openstack-glint-horizon','stop'])
    print "Remove /var/run/glint which have pids for service"
    [out,err] = execute_command(['rm','-rf','/var/run/glint'])
    print "Remove glint-service log files"
    [out,err] = execute_command(['rm','-rf','/var/log/glint-service'])

#read in conf and set global variables
cfg_f = yaml.load( open("glint_setup.yaml",'r') )
glint_url=cfg_f['glint-git-url']
horizon_url=cfg_f['glint-horizon-git-url']
gl_inst_type=cfg_f['glint-installation-type']
hor_inst_type=cfg_f['glint-horizon-installation-type']
gl_user_id=cfg_f['glint-user-id']
if len(sys.argv) == 2:
    print "Managing Glint using"
    print "glint url: %s"%glint_url
    print "glint-horizon url: %s"%horizon_url
    print "glint instance type: %s"%gl_inst_type
    print "glint-horizon instance type: %s"%hor_inst_type
    print "glint user id : %s"%gl_user_id

    if sys.argv[1] == 'install':
        print "Full Install of Glint and Glint Horizon"
        create_glint_user()
        download_install_glint()
        register_glint_in_openstack()
        start_glint_service()
    elif sys.argv[1] == 'uninstall':
        print "Full Removal of Glint and Glint Horizon"
        stop_glint_service()
        deregister_glint_in_openstack()
        delete_installed_glint()
        remove_glint_user()
    else:
        show_usage()
else:
    show_usage()


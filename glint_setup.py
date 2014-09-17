#!/usr/bin/python

import yaml,sys,subprocess,os

glint_url = ''
horizon_url = ''
gl_inst_type = ''
hor_inst_type= ''
gl_user_id=171

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

def download_install_glint():
    print "download install glint"
    [out,err] = execute_command(['python','glint_git_setup.py','install','%s'%glint_url,'%s'%horizon_url])

def register_glint_in_openstack():
    print "register glint in openstack"
    set_env_openstack_admin_pw()
    [out,err] = execute_command(['python','glint_openstack_registration.py'])

def setup_glint_as_a_service():
    print "setup glint as a service"

def remove_glint_user():
    print "remove glint user"
    [out,err] = execute_command(['python','glint_system_create_user.py','remove-glint-user','%s'%gl_user_id])

def delete_installed_glint():
    print "delete installed glint"
    [out,err] = execute_command(['python','glint_git_setup.py','uninstall'])

def deregister_glint_in_openstack():
    print "deregister glint in openstack"
    set_env_openstack_admin_pw()
    [out,err] = execute_command(['python','glint_openstack_registration.py','uninstall'])

def remove_glint_as_a_service():
    print "remove glint as a service"

def show_usage():
    print "Usage"
    print "INSTALL: python glint_setup.py install"
    print "UNINSTALL: python glint_setup.py uninstall"

#read in conf and set global variables
cfg_f = yaml.load( open("glint_setup.conf",'r') )
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
        setup_glint_as_a_service()
    elif sys.argv[1] == 'uninstall':
        print "Full Removal of Glint and Glint Horizon"
        remove_glint_as_a_service()
        deregister_glint_in_openstack()
        delete_installed_glint()
        remove_glint_user()
    else:
        show_usage()
else:
    show_usage()


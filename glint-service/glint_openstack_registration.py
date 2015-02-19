#!/usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
import os,re,sys,yaml
import subprocess

env_dict={}

glint_service_url='http://rat01.heprc.uvic.ca'
glint_service_port='9494'

cfg_dir = '/etc/glint'

def execute_command(cmd_args):
    process = subprocess.Popen(cmd_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = process.communicate()
    if err:
        print "warning: %s"%err
    return out,err

#ensure environment variables are set
def environment_check():
    tenant_id = os.getenv("OS_TENANT_ID")
    tenant_name = os.getenv("OS_TENANT_NAME")
    os_auth_url = os.getenv("OS_AUTH_URL")
    os_username = os.getenv("OS_USERNAME")
    os_password = os.getenv("OS_PASSWORD")
    
    if (tenant_id == None or tenant_name == None or os_auth_url == None or os_username == None or os_password == None):

        print "Missing Parameter Please check that tenantid, tenantname , authurl , username and password are set in the environment variables"
        return False
    return True

# use keystone to register glint as a service
def setup_glint_service():
    print "Setting Up Glint ... Remove any Old DB Entries"
    remove_glint_service()
    print "Registering Glint into Openstack's Keystone services and endpoint database"
    
    out,err = execute_command(['keystone','service-create','--name=glint','--type=image_mgt','--description="Image Distribution Service"'])
    rexp_processor = re.compile('\|\s+id\s+\|\s+[a-z0-9]{32}\s+\|')
    rexp_res = rexp_processor.search(out)
    rexp_processor = re.compile('[a-z0-9]{32}')
    glint_service_id = rexp_processor.search(rexp_res.group()).group()
    
    out,err = execute_command(['keystone','endpoint-create','--region=openstack','--service-id=%s'%glint_service_id,'--publicurl=%s:%s/image_dist/'%(glint_service_url,glint_service_port),'--internalurl=http://127.0.0.1:%s/'%glint_service_port,'--adminurl=%s:%s/admin'%(glint_service_url,glint_service_port)])
    print "Success Registering Glint to Openstack's Keystone database"
    return

def remove_glint_service():
    print "Remove and old registered glint services"
    process = subprocess.Popen(['keystone','service-list'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = process.communicate()
    if "glint" in out:
        print "Glint has been registered so lets remove it "
        rexp_processor = re.compile('\|\s+[a-z0-9]{32}\s+\|\s+glint\s+\|')
        rexp_res = rexp_processor.search(out)
        rexp_processor = re.compile('[a-z0-9]{32}')
        glint_service_id = rexp_processor.search(rexp_res.group()).group()
        #remove the glint_service_id using keystone using keystone service-delete id
        process = subprocess.Popen(['keystone','service-delete','%s'%glint_service_id],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = process.communicate()
        #locate the glint endpoint refenence using glint_service_id and delete using endpoint-delete id
        process = subprocess.Popen(['keystone','endpoint-list'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = process.communicate()
        if glint_service_id in out:
            regex_str = '\|\s+[a-z0-9]{32}\s+\|\s+\w+\s+\|\s+[a-zA-Z0-9:/._()-]+\s+\|\s+[a-zA-Z0-9:/._()-]+\s+\|\s+[a-zA-Z0-9:/._()-]+\s+\|\s+%s\s+\|'%glint_service_id
            rexp_processor = re.compile(regex_str)
            glint_endpoint_id = rexp_processor.search(out).group()
            process = subprocess.Popen(['keystone','endpoint-delete','%s'%glint_endpoint_id],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err = process.communicate()
    else:
        print "Glint has not been registered yet, so let's register it."
    return
env_ck = environment_check()

if not env_ck:
    cfg_f = yaml.load( open("%s/glint_setup.yaml"%cfg_dir,'r') )
    auth_file=cfg_f['glint-installation-auth']
    print "Environment variables are not set, try yaml conf file glint_setup.conf for an auth file %s"%auth_file
    [out,err] = execute_command(['cat',auth_file])
    for line in out.splitlines():
        exp_cmd = line.split('=',1)
        if len(exp_cmd) == 2:
            if "OS_USERNAME" in exp_cmd[0]:
                print "OS_USERNAME is %s"%exp_cmd[1] 
                env_dict['OS_USERNAME']=exp_cmd[1].replace('"','')
            elif "OS_TENANT_ID" in exp_cmd[0]:
                print "OS_TENANT_ID is %s"%exp_cmd[1]
                env_dict['OS_TENANT_ID']=exp_cmd[1]
            elif "OS_TENANT_NAME" in exp_cmd[0]:
                print "OS_TENANT_NAME is %s"%exp_cmd[1]
                env_dict['OS_TENANT_NAME']=exp_cmd[1].replace('"','')
            elif "OS_AUTH_URL" in exp_cmd[0]:
                print "OS_AUTH_URL is %s"%exp_cmd[1]
                env_dict['OS_AUTH_URL']=exp_cmd[1]
    if os.getenv("OS_PASSWORD") == None:
        print "Enter Openstack Admin Password "
        pw = sys.stdin.readline()
        env_dict['OS_PASSWORD']=pw.rstrip()
    else:
        print "Password Already Set "
        env_dict['OS_PASSWORD']=os.getenv("OS_PASSWORD")
    os.environ.update(env_dict)
    [out,err] = execute_command(['env'])
    print "env %s"%out
    env_ck=True

cfg_f = yaml.load( open("%s/glint_setup.yaml"%cfg_dir,'r') )
glint_service_url=cfg_f['glint-service-url']
glint_service_port=cfg_f['glint-service-port']

if env_ck:
    if len(sys.argv) == 2:
        if sys.argv[1] == 'uninstall':
            remove_glint_service()
        else:
            print "invalid argument ... only valid argument is uninstall"    
    else:
        setup_glint_service()
else:
    print "Unable to setup glint service for use by openstack becuase the environment variables need to be set by the administrator, please source the admins .rc file which you can get from the openstack horizon interface Access and Security section"



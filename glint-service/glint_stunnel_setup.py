#!/usr/bin/python
import subprocess,sys
from glint_arg_parser import GlintArgumentParser

pkg_dir = "glint-service"
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


gap = GlintArgumentParser()
gap.init_stunnel_arg_parser()
args = gap.parser.parse_args()

if args.install:
    print "Install stunnel"
    [out,err] = execute_command(['yum','install','stunnel'],'y')
    [out,err] = execute_command(['mkdir','/etc/stunnel'],None)
    [out,err] = execute_command(['openssl','req','-new','-x509','-days','365','-nodes','-out','/etc/stunnel/stunnel.pem','-keyout','/etc/stunnel/stunnel.pem'],'CA\nBC\nVIC\nUVIC\nHEPGC\nopenstack\nglint@glint.ca\n')
    [out,err] = execute_command(['/usr/bin/openssl','gendh','2048','>>','/etc/stunnel/stunnel.pem'],None)
    [out,err] = execute_command(['chmod','600','/etc/stunnel/stunnel.pem'],None)
    [out,err] = execute_command(['mkdir','/var/run/stunnel'],None)
    [out,err] = execute_command(['cp','%s/openstack-glint-stunnel'%pkg_dir,'/etc/init.d/.'],None)
    [out,err] = execute_command(['chmod','755','/etc/init.d/openstack-glint-stunnel'],None)
    [out,err] = execute_command(['cp','%s/dev_https'%pkg_dir,'/etc/stunnel/.'],None)
    [out,err] = execute_command(['service','openstack-glint-stunnel','start'],None)
    #[out,err] = execute_command(['stunnel','dev_https','&'],None)
    print "started stunnel "
elif args.uninstall:
    print "Uninstall stunnel"
    [out,err] = execute_command(['service','openstack-glint-stunnel','stop'],None)
    [out,err] = execute_command(['rm','-f','/etc/init.d/openstack-glint-stunnel'],None)
    [out,err] = execute_command(['rm','-rf','/var/run/stunnel'],None)
    [out,err] = execute_command(['yum','remove','stunnel'],'y')
    [out,err] = execute_command(['rm','-rf','/etc/stunnel'],None)
    


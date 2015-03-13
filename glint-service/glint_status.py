#!/bin/python

import subprocess

def execute_command(cmd_args):
    process = subprocess.Popen(cmd_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out,err = process.communicate()
    return out,err

print "List glint-horizon processes"
out,err = execute_command(['ps -fu glint'])
print out
print ""
print "List glint-server processes"
out,err = execute_command(['ps -fu root  | grep 9494'])
print out
print ""
print "Check for stunnel process"
out,err = execute_command(['ps -ef | grep stunnel'])
print out
print ""
print "Show Listening Ports 9494,8483,8080"
out,err = execute_command(['netstat -an | grep -e 8080 -e 8483 -e 9494 | grep LISTEN'])
print out
print ""


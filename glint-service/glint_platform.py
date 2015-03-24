#!/usr/bin/python

import platform

def isRedhat():
    if "redhat" in platform.platform():
        return True
    return False

def isUbuntu():
    if "Ubuntu" in platform.platform():
        return True
    return False

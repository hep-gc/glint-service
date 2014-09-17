#!/usr/bin/python

import argparse

class GlintArgumentParser:
    parser=None
 
    def __init__(self):
        print "init GlintArgumentParser"
        self.parser = argparse.ArgumentParser(description='Glints Argument Parser')
   
    def init_git_arg_parser(self):
        self.parser.add_argument("-install",nargs=1,choices=['all','glint','horizon'])
        self.parser.add_argument("-uninstall",nargs=1,choices=['all','glint','horizon'])
        self.parser.add_argument("-glint_url")
        self.parser.add_argument("-glint_hor_url")
        self.parser.add_argument("-glint_inst_type")
        self.parser.add_argument("-hor_inst_type")
        self.parser.add_argument("-glint_user_id")

#gap=GlintArgumentParser()
#args=gap.parser.parse_args()


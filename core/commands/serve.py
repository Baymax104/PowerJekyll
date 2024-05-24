# -*- coding: UTF-8 -*-

import os


class ServeCommand(object):

    def __init__(self, subparsers, root_dir, config):
        self.root_dir = root_dir
        self.config = config
        self.parser = subparsers.add_parser('serve', help='start blog server locally through jekyll.', aliases=['s'])
        self.parser.add_argument('-d', '--draft', help='start blog server with drafts.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        os.chdir(self.root_dir)
        command = 'bundle exec jekyll s'
        if args.draft:
            command += ' --drafts'
        os.system(command)
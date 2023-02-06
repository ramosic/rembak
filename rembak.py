#!/usr/bin/env python3
# Author: Christer Karlsen
# Email: chris@ramosicked.com
# Project: rembak
# Copyright (c) 2023, Christer Karlsen
# License: MIT License
#
#!/usr/bin/env python3

import os
import argparse
import logging
import sys
import random
import string

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--connect", help="connect to remote server", action="store_true")
    return parser.parse_args()

def copy_home_dir(args):
    ssh_config = os.path.expanduser("~/.ssh/config")
    if not os.path.isfile(ssh_config):
        logging.error("Error: .ssh/config file not found")
        return
    if not args.connect:
        logging.error("Error: argument must be either -c or --connect")
        return
    target_dir = "bak_" + ''.join(random.choices(string.hexdigits, k=2))
    target = "remote-server:{}".format(target_dir)
    try:
        os.system("scp -F {} $HOME {}".format(ssh_config, target))
        logging.info("Successfully copied home directory to {}".format(target_dir))
    except Exception as e:
        logging.error("Error: {}".format(e))
        logging.error("Check your permissions and try again")
        sys.exit(1)

if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(filename="output.log", level=logging.DEBUG,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    copy_home_dir(args)


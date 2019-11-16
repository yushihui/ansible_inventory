#!/usr/bin/env python

import argparse
import requests
import sys

try:
    import json
except ImportError:
    import simplejson as json


class NetBrainInventory(object):
    """NetBrain as a dynamic inventory for Ansible.
    Retrieves hosts list from netbrain API and returns Ansible dynamic inventory (JSON).
    """

    def __init__(self, url):
        self.api_url = url
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.get_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def get_inventory(self):

        if not self.api_url:
            sys.exit("Please provide a url")
        api_output = requests.get(self.api_url)
        api_output.raise_for_status()
        api_output_data = api_output.json()

        return api_output_data

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


NetBrainInventory("https://raw.githubusercontent.com/yushihui/ansible_inventory/master/sample.json")

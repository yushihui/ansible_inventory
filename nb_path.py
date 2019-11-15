import os
import sys
import requests


# try:
#     import requests
# except ImportError:
#     sys.exit('requests package is required for this inventory script.')

try:
    import json
except ImportError:
    import simplejson as json

class NetbBainsInventory(object):
    """NetBrain as a dynamic inventory for Ansible.
    Retrieves hosts list from netbrain API and returns Ansible dynamic inventory (JSON).
    """

    def __init__(self):
        self.api_url = ""

    @staticmethod
    def get_hosts_list(api_url):

        if not api_url:
            sys.exit("Please check API URL in script configuration file.")

        hosts_list = []
        api_output = requests.get(api_url)

        # Check that a request is 200 and not something else like 404, 401, 500 ... etc.
        api_output.raise_for_status()

        # Get api output data.
        api_output_data = api_output.json()

        if isinstance(api_output_data, dict) and "results" in api_output_data:
            hosts_list += api_output_data["results"]

        # Get hosts list.
        return hosts_list


def main():
    nb = NetbBainsInventory("")
    ansible_inventory = nb.generate_inventory()
    print(json.dumps(ansible_inventory))


if __name__ == "__main__":
    main()

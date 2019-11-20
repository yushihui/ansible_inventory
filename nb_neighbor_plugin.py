from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
import requests

DOCUMENTATION = '''
    name: nb_neighbor_plugin
    plugin_type: inventory
    short_description: nb inventory source
    description:
        - Get inventory hosts from the local nb_neighbor_plugin installation.
        - Uses a YAML configuration file that ends with nb_neighbor_plugin.(yml|yaml) or vbox.(yml|yaml).
        - The inventory_hostname is always the 'Name' of the nb_neighbor_plugin instance.
    extends_documentation_fragment:
      - constructed
      - inventory_cache
    options:
        plugin:
            description: token that ensures this is a source file for the 'nb_neighbor_plugin' plugin
            required: True
            choices: ['nb_neighbor_plugin']
        api_url:
            description: netbrain api url
            type: string
            default: 
        topology:
            description: network topology
'''

EXAMPLES = '''
# file must be named nb_neighbor.yaml or nb_neighbor.yml
plugin: nb_neighbor_plugin
groups:
  container: "'minis' in (inventory_hostname)"
'''


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'nb_neighbor_plugin'

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('nb_neighbor.yaml', 'nb_neighbor.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):

        super(InventoryModule, self).parse(inventory, loader, path, cache)
        config_data = self._read_config_data(path)
        self._consume_options(config_data)
        api_output = requests.get(self.get_option('api_url'))
        api_output.raise_for_status()
        api_output_data = api_output.json()
        host_data = api_output_data[self.get_option('topology')]
        for server in host_data:
            self.inventory.add_host(server['name'])
            self.inventory.set_variable(server['name'], 'ansible_host', server['ip'])




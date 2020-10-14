# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    inventory: host_list_from_env
    version_added: "2.9"
    short_description: Parses a 'host list' with ranges from environment var
    description:
        - Parses a host list string as a comma separated values of hosts and supports host ranges.
    options:
      host_list_var:
            description: List of hosts to parse
            required: True
            env:
              - name: HOST_LIST_VAR
'''

EXAMPLES = '''
    # simple range
    # HOST_LIST_VAR="foo.example.com,bar.exampe.com" ansible-playbook -i host_list_from_env.yml test.yml
'''

import os

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):

    NAME = 'host_list_var'

    def verify_file(self, host_list):

        return True

    def parse(self, inventory, loader, host_list, cache=True):
        ''' parses the inventory file '''

        super(InventoryModule, self).parse(inventory, loader, host_list)

        try:
            for h in self.get_option('host_list_var').split(','):
                h = h.strip()
                if h:
                    try:
                        (hostnames, port) = self._expand_hostpattern(h)
                    except AnsibleError as e:
                        self.display.vvv("Unable to parse address from hostname, leaving unchanged: %s" % to_text(e))
                        host = [h]
                        port = None

                    for host in hostnames:
                        if host not in self.inventory.hosts:
                            self.inventory.add_host(host, group='ungrouped', port=port)
        except Exception as e:
            raise AnsibleParserError("Invalid data from string, could not parse: %s" % to_native(e))

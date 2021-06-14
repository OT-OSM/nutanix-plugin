#!/usr/bin/python3
"""
An ansible module to call Nutanix VM create API
Author: Opstree Solutions
"""
import requests
from requests.auth import HTTPBasicAuth
from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = '''
---
module: nutanix_vm_create
short_description: Ansible module to create Nutanix VM
author:
    - Opstree Solutions (@opstree)
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
  - name: Test that nutanix vm create module
    nutanix_vm_create: 
      username: "abhishek"
      password:  "IamIronMan"
      nutanix_api_url: "http://nutanix.example.com"
      vm_name: "test-vm"
      power_state: "ON|OFF"
      num_sockets: 1
      num_vcpus_per_socket: 1
      num_threads_per_core: 1
      memory_size_mib: 1024

    register: result
  - debug: var=result    
'''

# pylint: disable=R0913
def create_nutanix_vm(vm_information):
    """create_nutanix_vm function creates a virtual machine in Nutanix"""
    json_data = {
        "spec": {
            "name": vm_information["vm_name"],
            "resources": {
                "num_sockets": vm_information["num_sockets"],
                "num_vcpus_per_socket": vm_information["num_vcpus_per_socket"],
                "num_threads_per_core": vm_information["num_threads_per_core"],
                "memory_size_mib": vm_information["memory_size_mib"],
                "power_state": vm_information["power_state"]
            }
        },
        "metadata": {
            "kind": "vm"
        }
    }

    request = requests.post(
        vm_information["nutanix_api_url"] + "/api/nutanix/v3/vms",
        auth=HTTPBasicAuth(vm_information["username"], vm_information["password"]),
        json=json_data
    )
    return request.json()

def run_nutanix_vm_creation_module():
    """This function will call the create VM API of nutanix"""
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        nutanix_api_url=dict(type='str', required=True),
        vm_name=dict(type='str', required=True),
        power_state=dict(type='str', required=False, default="ON"),
        num_sockets=dict(type='int', required=False, default=1),
        num_vcpus_per_socket=dict(type='int', required=False, default=1),
        num_threads_per_core=dict(type='int', required=False, default=1),
        memory_size_mib=dict(type='int', required=False, default=1024)
    )

    result = dict(changed=False, virtual_machine_information='', message='')

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

    try:
        build_info = create_nutanix_vm(module.params)
        result['virtual_machine_information'] = build_info
        result['message'] = 'Successfully executed vm creation API'

        module.exit_json(changed=True, results=result)
    except: # pylint: disable=W0702
        result['virtual_machine_information'] = {}
        result['message'] = 'Failed while executing vm creation API'
        module.fail_json(results=result, msg="Failed to execute task")

def main():
    """This is main function to call nutanix VM create API"""
    run_nutanix_vm_creation_module()

if __name__ == '__main__':
    main()

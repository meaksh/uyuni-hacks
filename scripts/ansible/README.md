**The scripts in this folder require:**
- "ansible_entitled" must be created (not as base entitlement) in the database
- "ansible_entitled" must be compatibly with bootstrap and salt entitlements
- This changes on the Java part: https://github.com/SUSE/spacewalk/commit/ab38d6c024d5b7ec5e6f936b602c54fbe6647c68
- This changes on Salt: https://github.com/openSUSE/salt/commit/7a97f103be5781c6cafd44ca099f7afa062a558a


=== Import Ansible inventory:
```console
suma41-srv:~ # python3 import_systems_from_ansible_controller.py -i /srv/susemanager/salt/salt_ssh/mgr_ssh_id -H suma41-ansible-controller.tf.local
```

=== Get "machine_id" grain using salt-ssh via controller node:
```console
suma41-srv:~ # salt-ssh --ssh-option='ProxyCommand="/usr/bin/ssh -i /srv/susemanager/salt/salt_ssh/mgr_ssh_id -o StrictHostKeyChecking=no -o User=root -W %h:%p suma41-ansible-controller.tf.local"' --roster=ansible --roster-file=/var/cache/ansible/ansible-inventory.yaml -N hybrid2 grains.get machine_id
```

=== Change machineId:
```console
suma41-srv:~ # python3 change_machine_id.py -m b451d3df0a2aa46841b03bcc5fad56c8 -s 1000010135
```

=== Final bootstrap of minion using controller as proxy:
```console
suma41-srv:~ # salt-ssh --ssh-option='ProxyCommand="/usr/bin/ssh -i /srv/susemanager/salt/salt_ssh/mgr_ssh_id -o StrictHostKeyChecking=no -o User=root -W %h:%p suma41-ansible-controller.tf.local"' --roster=ansible --roster-file=/var/cache/ansible/ansible-inventory.yaml -N hybrid2 state.apply certs,bootstrap pillar='{"mgr_server": "suma41-srv.tf.local", "minion_id": "suma41-ansible-sles15sp1-2.tf.local"}'
```


=== Know issues (salt-ssh):
- SSH key problems targetting "all" group
- Problems targetting single Ansible host

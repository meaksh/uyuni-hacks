reboot_transactional_system:
  local.system.reboot:
    - tgt: {{ data['id'] }}

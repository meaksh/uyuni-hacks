BEGIN;

insert into rhnServerGroupType (id, label, name, permanent, is_base)
   values (sequence_nextval('rhn_servergroup_type_seq'),
      'ansible_entitled', 'Ansible Management Entitled Servers',
      'N', 'N'
   );

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('i386-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('i386-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('i486-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('i586-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('i686-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('athlon-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('alpha-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('alpha-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('alphaev6-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ia64-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ia64-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('sparc-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('sparc-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('sparcv9-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('sparc64-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('s390-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
        values (lookup_server_arch('aarch64-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
        values (lookup_server_arch('armv7l-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
        values (lookup_server_arch('armv5tejl-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
        values (lookup_server_arch('armv6l-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
        values (lookup_server_arch('armv6hl-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('s390-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('s390x-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ppc-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('powerpc-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ppc64-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
    values (lookup_server_arch('ppc64le-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('pSeries-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('iSeries-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('x86_64-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ia32e-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('amd64-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('amd64-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('arm64-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ppc64iseries-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('ppc64pseries-redhat-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('arm-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('armv6l-debian-linux'),
            lookup_sg_type('ansible_entitled'));

insert into rhnServerServerGroupArchCompat ( server_arch_id, server_group_type )
	values (lookup_server_arch('mips-debian-linux'),
            lookup_sg_type('ansible_entitled'));


insert into rhnSGTypeBaseAddonCompat (base_id, addon_id)
values (lookup_sg_type('salt_entitled'),
        lookup_sg_type('ansible_entitled'));

insert into rhnSGTypeBaseAddonCompat (base_id, addon_id)
values (lookup_sg_type('foreign_entitled'),
        lookup_sg_type('ansible_entitled'));

insert into rhnServerGroup ( id, name, description, group_type, org_id )
 select nextval('rhn_server_group_id_seq'), sgt.name, sgt.name, sgt.id, X.org_id
 from rhnServerGroupType sgt,
    (select distinct msg.org_id
       from rhnServerGroup msg
      where msg.org_id not in (select org_id
                                 from rhnServerGroup sg
                                 join rhnServerGroupType sgt ON sgt.id = sg.group_type
                                where sgt.label = 'ansible_entitled')
    ) X
 where sgt.label = 'ansible_entitled';

COMMIT;

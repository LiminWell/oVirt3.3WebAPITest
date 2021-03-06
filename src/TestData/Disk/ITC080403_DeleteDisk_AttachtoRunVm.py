#encoding:utf-8

__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Wei Keke 
#---------------------------------------------------------------------------------
'''

import TestData.Disk.ITC08_SetUp as ModuleData

'''---------------------------------------------------------------------------------------------------
@note: PreData
---------------------------------------------------------------------------------------------------'''
sd_name = ModuleData.data1_nfs_name
cluster_name = ModuleData.cluster_nfs_name
vm_name = 'VM-ITC080403'
vm_info = '''
<vm>
        <name>%s</name>
        <description>Virtual Machine 2</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>%s</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <cpu>
            <topology sockets="2" cores="1"/>
        </cpu>
        <os>
            <boot dev="cdrom"/>
            <boot dev="hd"/>
        </os>
    </vm>
'''% (vm_name, cluster_name)

disk_name = 'DISK-ITC080403'
disk_info = '''
<disk>
    <alias>%s</alias>
    <name>%s</name>
    <storage_domains>
        <storage_domain>
            <name>%s</name>
        </storage_domain>
    </storage_domains>
    <size>1147483648</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''% (disk_name, disk_name, sd_name)

'''---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove Virtual Machine Disk. At least one of the VMs is not down.]</detail>
</fault>
'''
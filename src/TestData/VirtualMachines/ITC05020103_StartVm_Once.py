#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/03          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from TestData.VirtualMachines import ITC05_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''
vm_name = "vm-ITC0502010103"

xml_vm_info='''
<vm>
    <name>%s</name>
    <type>server</type>
    <memory>536870912</memory>
    <cluster>
        <name>%s</name>
    </cluster>
    <template>
        <name>Blank</name>
    </template>
    <cpu>
        <topology sockets="1" cores="1"/>
    </cpu>
    <os>
        <boot dev="cdrom"/>
        <boot dev="hd"/>
    </os>
</vm>
''' % (vm_name, ModuleData.cluster_nfs_name)

disk_alias = 'disk-ITC0502010103'
xml_disk_info = '''
<disk>
    <alias>%s</alias>
    <storage_domains>
        <storage_domain><name>%s</name></storage_domain>
    </storage_domains>
    <size>1073741824</size>
    <type>system</type>
    <interface>virtio</interface>
    <format>cow</format>
    <bootable>true</bootable>
</disk>
''' % (disk_alias, ModuleData.data1_nfs_name)

'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''
xml_start_vm_once = '''
    <action>
        <vm>
            <display>
                <type>spice</type>
            </display>
            <os>
                <boot dev="hd"/>
            </os>
        </vm>
    </action>
'''



'''
---------------------------------------------------------------------------------------------------
@note: Post-Test-Data
---------------------------------------------------------------------------------------------------
'''




'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_start_vm_once = 200



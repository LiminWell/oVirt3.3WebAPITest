#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/02          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from TestData.VirtualMachine import ITC05_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''
vm_name = "vm-ITC0501050102"

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


'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
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
expected_status_code_del_vm_up = 409
expected_info_del_vm_up = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove VM. VM is running.]</detail>
</fault>
'''

#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''
@note: PreData
'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
nw_name = 'network001'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)

profile_info = '''
<data_driver>
    <vnic_profile>
        <name>peanuts03</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
    <vnic_profile>
        <name>peanuts02</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
    
</data_driver>
'''

'''
@note: ExpectedData
'''
expected_status_code = 200

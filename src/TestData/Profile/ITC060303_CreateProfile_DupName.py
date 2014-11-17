#encoding:utf-8

from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestData.Profile import ITC06_SetUp as ModuleData

'''
@note: PreData
'''
nw_name = 'network_ITC06'
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)
profile_name = 'profile_ITC06'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)

profile_info = '''
    <vnic_profile>
        <name>profile_ITC06</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
'''
'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info = ''' 
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add VM network interface profile. The VM network interface profile's name is already used by an existing profile for the same network.
-Please choose a different name.]</detail>
</fault>
'''


#encoding:utf-8

__authors__ = ['wei keke']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                         
#---------------------------------------------------------------------------------
'''

import TestData.Network.ITC06_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''
@note: TestData
'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
nw_name = 'network001'
nw_info = '''
<data_driver>
    <network>
        <data_center id= "%s"/>    
    </network>
    <network>
        <name>%s</name>   
    </network>
</data_driver>
'''%(dc_id,nw_name)

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info_list =['''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Network [name] required for add</detail>
</fault>
'''
,
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Network [dataCenter.name|id] required for add</detail>
</fault>
'''
]

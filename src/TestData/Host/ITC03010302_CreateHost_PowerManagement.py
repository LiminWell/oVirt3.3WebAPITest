#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs import GlobalConfig
from TestAPIs.ClusterAPIs import ClusterAPIs
import ITC03_SetUp as DM

host1 = GlobalConfig.Hosts['node1']
host2 = GlobalConfig.Hosts['node4']

'''-----------------------------------------------------------------------------------------
@note: Pre-TestData
-----------------------------------------------------------------------------------------'''
host1_name = 'node-ITC03010302-1'
xml_host1_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster id="%s"/>
</host>
''' % (host1_name, host1['ip'], host1['password'], ClusterAPIs().getClusterIdByName(DM.cluster_name))


'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
# 配置电源管理选项的host2的相关信息
host2_name = 'node-ITC03010302-2'
xml_host2_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster id="%s"/>
    <power_management type="%s">
        <enabled>true</enabled>
        <address>%s</address>
        <username>%s</username>
        <password>%s</password>
    </power_management>
</host>
''' % (host2_name, \
       host2['ip'], \
       host2['password'], \
       ClusterAPIs().getClusterIdByName(DM.cluster_name), \
       host2['IMM']['type'], \
       host2['IMM']['ip'], \
       host2['IMM']['user'], \
       host2['IMM']['password']
       )

'''-----------------------------------------------------------------------------------------
@note: Post-TestData
-----------------------------------------------------------------------------------------'''
# 资源清理时删除host所用的选项（强制删除/同步）
xml_host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
expected_status_code_create_host = 201          # 创建主机操作的期望状态码
expected_status_code_deactive_host = 200        # 维护主机操作的期望状态码
expected_status_code_del_host = 200             # 删除主机操作的期望状态码

#encoding:utf-8


__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/24          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

'''
----------------------------------------------------------------------------------
@note: TestData
----------------------------------------------------------------------------------
'''
dc_name = ['DC-ITC01010301-NFS', 'DC-ITC01010301-ISCSI', 'DC-ITC01010301-FC']

dc_info = '''
<data_driver>
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="3" major="3"/>
    </data_center>
    <data_center>
        <name>%s</name>
        <storage_type>iscsi</storage_type>
        <version minor="2" major="3"/>
    </data_center>
    <data_center>
        <name>%s</name>
        <storage_type>fcp</storage_type>
        <version minor="1" major="3"/>
    </data_center>
</data_driver>
''' % (dc_name[0], dc_name[1], dc_name[2])

'''
----------------------------------------------------------------------------------
@note: ExpectedResult
----------------------------------------------------------------------------------
'''
status_code = 201
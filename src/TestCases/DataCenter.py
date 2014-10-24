#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/23          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import unittest

import xmltodict

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs, smart_attach_storage_domain, smart_deactive_storage_domain, smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestCases.Host import smart_create_host, smart_del_host
from TestCases.StorageDomain import smart_create_storage_domain, smart_del_storage_domain, smart_deactive_storage_domain
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare


class ITC01_SetUp(BaseTestCase):
    '''
    @summary: 数据中心模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个NFS类型数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建3个存储域（data1/data2/ISO/Export）；
    @note: （5）将 data1 附加到数据中心。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()

    def test_CreateModuleTestEnv(self):
        '''
        @summary: 创建DataCenter模块测试环境
        '''
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        
        # 创建1个数据中心（nfs类型）
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def create_data_centers(xml_dc_info):
            LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % xmltodict.parse(xml_dc_info)['data_center']['name'])
            self.assertTrue(dcapi.createDataCenter(xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
        create_data_centers()
        
        # 创建1个集群
        @BaseTestCase.drive_data(self, self.dm.cluster_info)
        def create_clusters(xml_cluster_info):
            LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (xmltodict.parse(xml_cluster_info)['cluster']['name'], xmltodict.parse(xml_cluster_info)['cluster']['data_center']['name']))
            self.assertTrue(capi.createCluster(xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
        create_clusters()
        
        # 在NFS数据中心中创建一个主机，并等待主机UP。
        @BaseTestCase.drive_data(self, self.dm.hosts_info_xml)
        def create_hosts(xml_host_info):
            LogPrint().info("Pre-Module-Test-3: Create Host '%s' in Cluster '%s'." % (xmltodict.parse(xml_host_info)['host']['name'], xmltodict.parse(xml_host_info)['host']['cluster']['name']))
            self.assertTrue(smart_create_host(xmltodict.parse(xml_host_info)['host']['name'], xml_host_info))
        create_hosts()
        
        # 为NFS数据中心分别创建Data（data1/data2）/ISO/Export域。
        @BaseTestCase.drive_data(self, self.dm.xml_datas_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % (sd_name))
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
        
        # 将创建的的data1附加到NFS/ISCSI数据中心里。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))

    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC010101_GetDCList(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-01获取数据中心列表
    '''
    def test_GetDataCentersList(self):
        dcapi = DataCenterAPIs()
        r = dcapi.getDataCentersList()
        if r['status_code']==200:
            LogPrint().info('Get DataCenters list SUCCESS.')
        else:
            LogPrint().error('Get DataCenters list FAIL.')
            self.flag = False
        self.assertTrue(self.flag)
        
class ITC010102_GetDCInfo(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-02获取指定数据中心信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 准备1：创建一个数据中心
        self.dcapi = DataCenterAPIs()
        self.dcapi.createDataCenter(self.dm.dc_info)
        
    def test_GetDataCenterInfo(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取数据中心的信息，并与期望结果进行对比
        r = self.dcapi.getDataCenterInfo(self.dm.dc_name)
        if r['status_code']==200:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.dc_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Get DataCenter '%s' info SUCCESS." % self.dm.dc_name)
            else:
                LogPrint().error("Get DataCenter '%s' info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get/Create DataCenter '%s' FAILED. " % self.dm.dc_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name):
            self.dcapi.delDataCenter(self.dm.dc_name)

class ITC01010301_CreateDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-01正常创建
    @note: 包括3种类型数据中心（NFS、ISCSI和FC）
    @note: 包括3种兼容版本（3.1、3.2、3.3）
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateDC(self):
        '''
        @summary: 测试用例执行步骤
        '''     
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def do_test(xml_info):
            self.flag = True
            dc_name = xmltodict.parse(xml_info)['data_center']['name']
            r = self.dcapi.createDataCenter(xml_info)
            if r['status_code']==self.dm.status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(xml_info), r['result']):
                    LogPrint().info("Create DataCenter '%s' SUCCESS." % dc_name)
                else:
                    LogPrint().error("Create DataCenter '%s' SUCCESS, but DataCenter info INCORRECT." % dc_name)
                    self.flag = False
            else:
                LogPrint().error("Create DataCenter '%s' FAILED. " % dc_name)
                self.flag = False
            self.assertTrue(self.flag)
            
        do_test()
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        for dc in self.dm.dc_name:
            if self.dcapi.searchDataCenterByName(dc):
                self.dcapi.delDataCenter(dc)
                
class ITC01010302_CreateExistDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-02重复创建
    @note: 创建重名的数据中心（与Default重名）
    @precondition: 存在缺省的数据中心Default
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateExistDC(self):
        '''
        @summary: 创建重名数据中心（Default），检查接口返回的状态码以及提示信息是否符合预期。
        '''
        r = self.dcapi.createDataCenter(self.dm.dc_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when create exist DC.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when create exist DC.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理（本次测试没有需要清理的资源）
        '''
        BaseTestCase.tearDown(self)
        
class ITC0101030301_CreateDC_NoRequiredParams(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-03参数验证-01缺少必填参数
    @note: 创建数据中心，缺少必需要的参数（数据中心有3个必需参数：名称、存储域、兼容版本），验证接口返回状态码及提示信息是否符合预期。
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateDCWithoutRequiredParams(self):
        '''
        @summary: 创建数据中心，缺少必需要的参数（数据中心有3个必需参数：名称、存储域、兼容版本），检查接口返回的状态码以及提示信息是否符合预期。
        '''
        # 本用例有3种测试情况，所以期望结果也有3种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def do_test(xml_info):
            self.flag = True
            r = self.dcapi.createDataCenter(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: The returned status code and messages are CORRECT.")
                else:
                    LogPrint().error("FAIL: The returned messages are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
            
        do_test()
    
    def tearDown(self):
        '''
        @summary: 资源清理（本次测试没有需要清理的资源）
        '''
        BaseTestCase.tearDown(self)   
        
class ITC0101030302_CreateDC_VerifyName(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-03参数验证-02名称有效性验证
    @note: 
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateDC_VerifyName(self):
        '''
        @summary: 创建数据中心，验证数据中心名称参数有效性
        '''
        # 本用例有多种测试情况，所以期望结果也有多种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def do_test(xml_info):
            self.flag = True
            r = self.dcapi.createDataCenter(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: The returned status code and messages are CORRECT.")
                else:
                    LogPrint().error("FAIL: The returned messages are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
            
        do_test()
    
    def tearDown(self):
        '''
        @summary: 资源清理（本次测试没有需要清理的资源）
        '''
        pass

class ITC01010401_UpdateUninitializedDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-04编辑-01编辑Uninitialized状态数据中心
    @note: Uninitialized数据中心的每一项均可编辑，这里重点测试name、description、type以及version等4项
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.pre_dc_name)
        self.dcapi.createDataCenter(self.dm.pre_dc_info)
        
    def test_UpdateUninitializedDC(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：编辑Uninitialized数据中心
        STEP 2：验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     

        self.flag = True
        r = self.dcapi.updateDataCenter(self.dm.pre_dc_name, self.dm.test_dc_info)
#         print r['status_code']
#         print xmltodict.unparse(r['result'], pretty=True)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.test_dc_info), r['result']):
                LogPrint().info("PASS: Update DataCenter SUCCESS.")
            else:
                LogPrint().error("FAIL: Update DataCenter FAIL, the actual dc info not equals to expected.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code of update operation INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        for dc_name in [self.dm.pre_dc_name, self.dm.test_dc_name]:
            if self.dcapi.searchDataCenterByName(dc_name)['result']['data_centers']:
                LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % dc_name)
                self.dcapi.delDataCenter(dc_name)
            
class ITC01010403_UpdateDC_DupName(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-04编辑-03数据中心重名
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create 2 DataCenters '%s and %s'." % (self.dm.dc_name_list[0], self.dm.dc_name_list[1]))
        
        @BaseTestCase.drive_data(self, self.dm.pre_dc_info)
        def do_test(xml_info):
            self.dcapi.createDataCenter(xml_info)
            
        do_test()
        
    def test_UpdateUninitializedDC(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：将一个DC名称编辑为另一个已存在的DC名称
        STEP 2：验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.updateDataCenter(self.dm.target_dc_name, self.dm.test_dc_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when Update DC with a Dup name.")
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL, The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        for dc_name in self.dm.dc_name_list:
            if self.dcapi.searchDataCenterByName(dc_name)['result']['data_centers']:
                LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % dc_name)
                self.dcapi.delDataCenter(dc_name)
                
class ITC01010404_UpdateDCVersion_HighToLow(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-04编辑-04兼容版本由高到低
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s' with high version.")
        self.dcapi.createDataCenter(self.dm.pre_dc_info)

    def test_UpdateDCVersion_HighToLow(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：将一个低版本的数据中心修改为高版本
        STEP 2：操作失败，验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.updateDataCenter(self.dm.dc_name, self.dm.update_dc_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when Update DC to lower version.")
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL. The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % self.dm.dc_name)
            self.dcapi.delDataCenter(self.dm.dc_name)
            
class ITC01010501_DelDC_Uninitialized(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-05删除-01常规删除
    @note: 删除Uninitialized状态的数据中心
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.dc_name)
        # PreStep-01：创建一个数据中心，其状态为Uninitialized
        self.dcapi.createDataCenter(self.dm.pre_dc_info)
        
    def test_DelDC_Uninitialized(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：删除一个Uninitialized状态的数据中心
        STEP 2：操作成功，验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.delDataCenter(self.dm.dc_name)
        if r['status_code']==self.dm.expected_status_code:
            if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers'] is None:
                LogPrint().info("PASS: Returned status code is CORRECT and Delete DC SUCCESS.")
            else:
                LogPrint().error("FAIL: Delete DC FAILED, the DC still exists.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL. The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % self.dm.dc_name)
            self.dcapi.delDataCenter(self.dm.dc_name)
      
class ITC01010502_DelDC_Force(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-05删除-02强制删除
    @note: 强制删除Uninitialized状态的数据中心
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.dc_name)
        # PreStep-01：创建一个数据中心，其状态为Uninitialized
        self.dcapi.createDataCenter(self.dm.pre_dc_info)
        
    def test_DelDC_Uninitialized(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：强制删除一个Uninitialized状态的数据中心
        STEP 2：操作成功，验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.delDataCenter(self.dm.dc_name, self.dm.del_dc_option)
        if r['status_code']==self.dm.expected_status_code:
            if not self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
                LogPrint().info("PASS: Force-Delete DC SUCCESS. Returned status code is CORRECT.")
            else:
                LogPrint().error("FAIL: Force-Delete DC FAILED, the DC still exists.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL. The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % self.dm.dc_name)
            self.dcapi.delDataCenter(self.dm.dc_name)

class ITC010201_GetSDListOfDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-01查看存储域列表
    @todo: 未完成
    '''
    def setUp(self):
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        self.sdapi = StorageDomainAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.dc_name)
        # PreStep-01：创建一个数据中心，其状态为Uninitialized
        self.dcapi.createDataCenter()
        




if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["DataCenter.ITC01010502_DelDC_Force"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

#     fileName = r"d:\result.html"
#     fp = file(fileName, 'wb')
#     runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
#     runner.run(testSuite)
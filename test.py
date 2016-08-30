import unittest
from apkparser import apkparser
import numpy as np

class test_apkparser(unittest.TestCase):

    # init self variable
    # write init like this to ignore duplicate with unittest init. http://stackoverflow.com/questions/17353213/init-for-unittest-testcase
    def __init__(self, *args, **kwargs):
        super(test_apkparser, self).__init__(*args, **kwargs)
        self.ap = apkparser('test.apk')
        self.class_item_list = self.ap.get_class_item_list('Lcom/alipay/sdk/util')
    
    # test apkparser.get_pkg_class_dict()
    def test_get_pkg_class_dict(self):
       pkg_class_dict = self.ap.get_pkg_class_dict()
       pkg_count = len(pkg_class_dict) 
       class_count = 0
       for k in pkg_class_dict:
           c = pkg_class_dict[k]
           class_count += len(c)

       self.assertEqual(pkg_count, 109)
       self.assertEqual(class_count, 1680)

    def test_get_class_count(self):
        c = self.ap.get_class_count('Lcom/alipay/sdk/util')
        self.assertEqual(c, 12)
        
        c = self.ap.get_class_count('not/a/pkg')
        self.assertEqual(c, -1)
        
    def test_get_pkg_depth(self):
        self.assertEqual(self.ap.get_pkg_depth('Lcom/alipay/sdk/util'), 4)
        self.assertEqual(self.ap.get_pkg_depth('Lcom/alipay/sdk'), 3)

    def test_get_class_size_sum(self):
        self.assertEqual( self.ap.get_class_size_sum(self.class_item_list), 384 )

    def test_get_class_interface_count_sum(self):
        self.assertEqual( self.ap.get_class_interface_count_sum(self.class_item_list), 2 )
        
    def test_get_class_methods_count_sum(self):
        self.assertEqual( self.ap.get_class_methods_count_sum(self.class_item_list), 64 )

    def test_get_class_virtual_method_count_sum(self):
        self.assertEqual( self.ap.get_class_virtual_method_count_sum(self.class_item_list), 12 )

    def test_get_class_variable_count_sum(self):
        self.assertEqual( self.ap.get_class_variable_count_sum(self.class_item_list), 46 )

    def test_get_class_instance_variable_count_sum(self):
        self.assertEqual( self.ap.get_class_instance_variable_count_sum(self.class_item_list), 20 )

    def test_get_class_static_variable_count_sum(self):
        self.assertEqual( self.ap.get_class_static_variable_count_sum(self.class_item_list), 26 )

    def test_get_class_access_flag_count_sum(self):
        self.assertEqual( self.ap.get_class_access_flag_count_sum(self.class_item_list), 16569 )

    def test_get_class_name_array(self):
        class_name_arr = self.ap.get_class_name_array(self.class_item_list)
        expected_result = np.array([2.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0])
        for i in range(10):
            self.assertEqual( class_name_arr[i], expected_result[i] )

    def test_get_class_super_class_name_array(self):
        class_name_arr = self.ap.get_class_super_class_name_array(self.class_item_list)
        expected_result = np.array( [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0] )
        for i in range(10):
            self.assertEqual( class_name_arr[i], expected_result[i] )




    def test_get_method_native_function_count_sum(self):
        self.assertEqual( self.ap.get_method_native_function_count_sum(self.class_item_list), 0 )
    
    def test_get_method_para_num_array(self):
        expected_result = np.array( [34, 32, 8, 0, 2, 0, 0, 0, 0, 0] )
        rt = self.ap.get_method_para_num_array(self.class_item_list)
        for i in range(10):
            self.assertEqual( rt[i], expected_result[i] )
 
    def test_get_method_access_info_array(self):
        expected_result = np.array( [39, 26, 12, 0, 15, 47, 0, 5, 0, 0, 0, 0] )
        rt = self.ap.get_method_access_info_array(self.class_item_list)
        for i in range(10):
            self.assertEqual( rt[i], expected_result[i] )




if __name__ == '__main__':
    unittest.main()





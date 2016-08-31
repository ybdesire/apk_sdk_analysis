import os
import sys
import pickle

androguard_module_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'common/Androguard-2.0/androguard' )

if not androguard_module_path in sys.path:
    sys.path.append(androguard_module_path)


from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis
from sklearn.feature_extraction import FeatureHasher

__author__ = 'Bin Yin (ybdesire@gmail.com)'
__date__ = '2016-08-26'
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(i) for i in __version_info__)


class apkparser:

    def __init__(self, file_name):
        self.a = apk.APK(file_name)
        self.d = dvm.DalvikVMFormat(self.a.get_dex())
        self.x = analysis.VMAnalysis(self.d)
        
        self.pkg_class_dict = {}

    # package level info
    # key-value of package name, class item list
    def get_pkg_class_dict(self):
        pkgs_class = []
        pkgs = set()
        pkg_dict = {}
        for c in self.d.get_classes():
            s = c.get_name()
            pkgs_class.append(s)
            pkg_without_classinfo = s.replace('/{}'.format(s.split('/')[-1]), '')
            pkgs.add(pkg_without_classinfo)
            if pkg_without_classinfo not in pkg_dict:
                pkg_dict[pkg_without_classinfo] = []
            pkg_dict[pkg_without_classinfo].append(c)
        
        self.pkg_class_dict = pkg_dict
        return self.pkg_class_dict


    # package level info
    # return the class count at the package
    def get_class_count(self, pkg_name):
        if not self.pkg_class_dict: # dict is empty
            self.get_pkg_class_dict()
        if pkg_name in self.pkg_class_dict:
            return len(self.pkg_class_dict[pkg_name])
        else:
            print('pkg_name is not exists')
            return -1
            

    # package level info
    # the depth of 'Lcom/jeremyfeinstein/slidingmenu/lib' is 4
    def get_pkg_depth(self, pkg_name):
        return len(pkg_name.split('/'))

    
    # class level info
    # get all class size sum 
    def get_class_size_sum(self, class_item_list):
        size_sum = 0
        for class_item in class_item_list:
            size_sum += class_item.get_length()
        return size_sum


    # internal use
    # get class_item_list by package name 
    def get_class_item_list(self, pkg_name):
        if not self.pkg_class_dict: # dict is empty
            self.get_pkg_class_dict()
        if pkg_name in self.pkg_class_dict:
            return self.pkg_class_dict[pkg_name]
        else:
            return null
    

    # class level info
    def get_class_interface_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += len( class_item.get_interfaces() )
        return count_sum


    # class level info
    def get_class_methods_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += class_item.get_class_data().get_direct_methods_size()
        return count_sum

    # class level info
    def get_class_virtual_method_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += class_item.get_class_data().get_virtual_methods_size()
        return count_sum


    # class level info
    def get_class_variable_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += len( class_item.get_fields() )
        return count_sum


    # class level info
    def get_class_instance_variable_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += class_item.get_class_data().get_instance_fields_size()
        return count_sum

        
    # class level info
    def get_class_static_variable_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += class_item.get_class_data().get_static_fields_size()
        return count_sum


    # class level info
    def get_class_access_flag_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            count_sum += class_item.get_access_flags()
        return count_sum


    # class level info
    # return array[10], float type
    def get_class_name_array(self, class_item_list):
        D=[{}]
        for class_item in class_item_list:
           class_name = class_item.get_name()
           D[0][class_name] = 1
        h = FeatureHasher(n_features=10, non_negative=True)
        f = h.transform(D)
        return f.toarray()[0]

   
    # class level info
    # return array[10], float type
    def get_class_super_class_name_array(self, class_item_list):
        D=[{}]
        for class_item in class_item_list:
           class_name = class_item.get_superclassname()
           D[0][class_name] = 1
        h = FeatureHasher(n_features=10, non_negative=True)
        f = h.transform(D)
        return f.toarray()[0]
    

    # method level info
    def get_method_native_function_count_sum(self, class_item_list):
        count_sum = 0
        for class_item in class_item_list:
            methods = class_item.get_methods()
            for m in methods:
                fun_access_str = m.get_access_flags_string() # such as 'public static'
                if 'native' in fun_access_str:
                    count_sum += 1
        return count_sum

    # method level info
    # return [34, 32, 8, 0, 2, 0, 0, 0, 0, 0], means they are 34 functions with void parameter, and 32 functions with 1 parameter, and 8 functions with 2 parameters, ...
    def get_method_para_num_array(self, class_item_list):
        result = [0]*10

        for class_item in class_item_list:
            methods = class_item.get_methods()
            for m in methods:
                fun_info = m.get_information()
                if('params' in fun_info):
                    param_count = len( fun_info['params'] )
                    if(param_count>=9):
                        result[9] += 1
                    else:
                        result[param_count] += 1
                else:
                    result[0] += 1
        return result


    # method level info
    # 
    def get_method_access_info_array(self, class_item_list):
        '''
        public
        private
        final
        abstract
        constructor
        static
        synchronized
        synthetic
        bridge
        varargs
        0x0
        protected
        '''
        result = [0]*12
        for class_item in class_item_list:
            methods = class_item.get_methods()
            for m in methods:
                access_info_list = m.get_access_flags_string().split(' ')
                for a in access_info_list:
                    if(a=='public'):
                        result[0] += 1
                    elif(a=='private'):
                        result[1] += 1
                    elif(a=='final'):
                        result[2] += 1
                    elif(a=='abstract'):
                        result[3] += 1
                    elif(a=='constructor'):
                        result[4] += 1
                    elif(a=='static'):
                        result[5] += 1
                    elif(a=='synchronized'):
                        result[6] += 1
                    elif(a=='synthetic'):
                        result[7] += 1
                    elif(a=='bridge'):
                        result[8] += 1
                    elif(a=='varargs'):
                        result[9] += 1
                    elif(a=='0x0'):
                        result[10] += 1
                    else:
                        result[11] += 1
        return result

 
    
    def get_sensitive_api_info(self, class_item_list):
        class_item_names = []
        for class_item in class_item_list:
            class_item_names.append( class_item.get_name() )

        api_list = pickle.load( open('api_list.p', 'rb') )
        result = [0]*len(api_list)
        count = 0
        for api in api_list:
            class_pattern = api[0]
            method_pattern = api[1]
            paths = self.x.get_tainted_packages().search_methods(class_pattern, method_pattern, '.') 
            class_names = []
            for p in paths:
                i = p.get_src_idx()
                m = self.d.get_method_by_idx(i)
                class_names.append( m.get_class_name() )
            for c in class_names:
                if c in class_item_names:
                    result[count] += 1
            count += 1
        return result


if __name__ == '__main__':
    pass






import os
import sys

androguard_module_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'common/Androguard-2.0/androguard' )

if not androguard_module_path in sys.path:
    sys.path.append(androguard_module_path)


from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis


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
        print('len pkgs_class: {}'.format(len(pkgs_class)))
        print('len pkgs: {}'.format(len(pkgs)))
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
    def get_class_size_sum(class_item_list):
        size_sum = 0
        for class_item in class_item_list:
            size_sum += class_item.get_length()
        return size_sum






if __name__ == '__main__':
    pass


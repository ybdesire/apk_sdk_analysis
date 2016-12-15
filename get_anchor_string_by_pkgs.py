import os
import sys
import numpy as np
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


file_path = '/home/bin_yin/test.apk'
pkg_list = ['Lcom.umeng.analytics.a', 'Lcom.umeng.analytics']

a = apk.APK(file_path)
d = dvm.DalvikVMFormat(a.get_dex())
x = analysis.VMAnalysis(d)

strs_pkgs = set()
strs_others = set()

for pkg in pkg_list:
    strs = x.tainted_variables.get_strings()
    for s in strs:
        for path in s[0].get_paths():
            cm_method = d.get_cm_method(path[1])
            cm_method_name = cm_method[0].replace('/', '.')
            if(cm_method_name.find(pkg)!=-1):
                strs_pkgs.add(s[1])
                #print('{0}:  {1}'.format(pkg, s[1]))
            else:
                strs_others.add(s[1])
print(strs_pkgs-strs_others)

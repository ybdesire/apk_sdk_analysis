import os
import sys

androguard_module_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'common/Androguard-2.0/androguard' )

if not androguard_module_path in sys.path:
    sys.path.append(androguard_module_path)


from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis



sp = '../samples_balanced/00000b633c4c584045874073da8a142c8c79a2bf'

def get_androguard_obj(apkfile):
    a = apk.APK(apkfile, False, "r", None, 2)
    d = dvm.DalvikVMFormat(a.get_dex())
    x = analysis.VMAnalysis(d)
    return (a,d,x)

def get_packages(x):
    pkgs_class = []
    pkgs = set()
    pkg_dict = {}
    for m, s in x.get_tainted_packages().get_packages():
        pkgs_class.append(s)
        pkg_without_classinfo = s.replace('/{}'.format(s.split('/')[-1]), '')
        pkgs.add(pkg_without_classinfo)
        if pkg_without_classinfo not in pkg_dict:
            pkg_dict[pkg_without_classinfo] = []
        pkg_dict[pkg_without_classinfo].append(s)

    print('len pkgs_class: {}'.format(len(pkgs_class)))
    print('len pkgs: {}'.format(len(pkgs)))
    return pkg_dict

    

if __name__=='__main__':
    ao = get_androguard_obj(sp)
    x = ao[2]
    pkgs_dict = get_packages(x)
    #print(pkgs_dict)
    res  = x.get_tainted_packages().search_packages('Landroid/support/v4/widget')
    print( analysis.show_Paths(ao[1], res[0]) )










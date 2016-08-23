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


if __name__=='__main__':
    ao = get_androguard_obj(sp)
    x = ao[2]
    pkgs = x.get_tainted_packages()
    for pkg in pkgs.get_packages():
        print(pkg)
    









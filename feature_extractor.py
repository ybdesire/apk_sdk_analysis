from apkparser import apkparser
import joblib as jl
import numpy as np
import os
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing

__author__ = 'Bin Yin (ybdesire@gmail.com)'
__date__ = '2016-09-01'
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(i) for i in __version_info__)


invalid_ids = ['00005018bcdab5db5b0268095badbe46b97ddc7d','003541a51286a91e186992df1f2aedab5cac43b8']

def extract_features(feature_extractor, ids, num, cfg=None):
    count = 0
    print('started: process-{}'.format(num))
    for apk_id in tqdm(ids):
        if apk_id not in invalid_ids:
            print('ing for: {}'.format(apk_id))
            ap = apkparser(os.path.join(feature_extractor.src, '{}'.format(apk_id)))
            pcd = ap.get_pkg_class_dict()
            for pkg in pcd:
                fea1 = feature_extractor.get_package_fea(ap, pkg)
                fea2 = feature_extractor.get_class_fea(ap, pkg)
                fea3 = feature_extractor.get_method_fea(ap, pkg)
            count += 1
            print('process-{}, {}/{}'.format(num, count, len(ids)+1))
             
            #print('{}'.format(apk_id))
            #print('{}\n'.format(pkg))
            #print('{}'.format(np.hstack( (fea1,fea2,fea3) )))
            #print('\n\n')
            

class feature_extractor:
    
    def __init__(self, apk_files_path, dst, samples_id_file):
        self.src = apk_files_path
        self.dst = dst
        self.id_list = []
        with open(samples_id_file, 'r') as f:
            for i in f:
                self.id_list.append(i.replace('\n', ''))
   
    def get_package_fea(self, apkobj, pkg_name):
        r1 = apkobj.get_package_name_array(pkg_name) # 10
        r2 = np.array( [apkobj.get_class_count(pkg_name)] )# 1
        r3 = np.array( [apkobj.get_pkg_depth(pkg_name)] ) # 1
        return np.hstack( (r1, r2, r3) )


    def get_class_fea(self, apkobj, pkg_name):
        class_item_list = apkobj.get_class_item_list(pkg_name)
        r1 = np.array( [apkobj.get_class_size_sum(class_item_list)] )
        r2 = np.array( [apkobj.get_class_interface_count_sum(class_item_list)] )
        r3 = np.array( [apkobj.get_class_methods_count_sum(class_item_list)] )
        r4 = np.array( [apkobj.get_class_virtual_method_count_sum(class_item_list)] )
        r5 = np.array( [apkobj.get_class_variable_count_sum(class_item_list)] )
        r6 = np.array( [apkobj.get_class_instance_variable_count_sum(class_item_list)] )
        r7 = np.array( [apkobj.get_class_static_variable_count_sum(class_item_list)] )
        r8 = np.array( [apkobj.get_class_access_flag_count_sum(class_item_list)] )
        r9 = apkobj.get_class_name_array(class_item_list)
        r10 = apkobj.get_class_super_class_name_array(class_item_list)
        return np.hstack( (r1, r2, r3, r4, r5, r6, r7, r8, r9, r10) )

    def get_method_fea(self, apkobj, pkg_name):
        class_item_list = apkobj.get_class_item_list(pkg_name)
        r1 = np.array( [apkobj.get_method_native_function_count_sum(class_item_list)] ) # 1
        r2 = apkobj.get_method_para_num_array(class_item_list) # 10
        r3 = apkobj.get_method_access_info_array(class_item_list) # 12
        r4 = apkobj.get_sensitive_api_info(class_item_list) # 32
        return np.hstack( (r1, r2, r3, r4) )        

    def get_features(self, jobs=8, cfg=None):
        P = Pool(processes=jobs)
        id_list_len = len(self.id_list)
        for i in range(jobs):
            ids = self.id_list[ int(id_list_len*i/8):int(id_list_len*(i+1)/8) ]
            P.apply_async(extract_features, (self, ids, i))
        P.close()
        P.join()
        



if __name__ == '__main__':
    fe = feature_extractor( '../samples_balanced/', 'features', '../samples_balanced/samples_id.txt' )
    print('len={}\n'.format(len(fe.id_list)))
    fe.get_features()

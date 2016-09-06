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


invalid_ids = ['00005018bcdab5db5b0268095badbe46b97ddc7d','003541a51286a91e186992df1f2aedab5cac43b8', '0005133cdecf65d12cf57608cee96f70fa42d459', '0005133cdecf65d12cf57608cee96f70fa42d459', '00873563bafb16ccdb66a6165cfc7b1d81960f92', '0000d04e67ae13619e80bdd27c6b196d0536b662', '000b5fb2cc935948f09bf84309378a1764c80287', '0001943ae9d682473ee90729b6e2a77e006804ca', '0013122f939c66cadf483fab19c1fe04a2dce01d', '0021a895f1ff34c6e693eba2f193693de5550b6f', '003879a8d69ac6e118da2c93f441188aeaa76fb4', '0009f1b6f503c0b16e8125fbe0261044233ffaf6', '008cca6982435050356f0eb566c8b8ba6bde114b', '000bc485896a55a866b7b266ae60020d881c88fc', '0001f7d6cf964c058e162b6ef2b00ee3fb9c2524', '002258754059564d1169c418e432be087b54dc7e', '00389cc6f878d7992445b92b9967ae9ec9c66c0d', '000b58836c16e2b9e99b8efda16096cc3015e948', '008d6abce3efee889bce2c14f14e72682b72f44a', '000169aa2c800961c83e795e3b90bf840500092a', '000bfc16f3386a70f338e214e8fb795266b2212f', '0002b32760f90b69749da69c20a137dfcbce4128', '0014da4438393dc6240b0277f38e633063e3ba21', '0024bbe054cee8f04c1194808c6344384fc37a27', '00396006470b33677754af1c88d82690fb33f6a9', '000f85dc002d495cce4ad4ab41710843ea416306', '008ef8534e2be26182dc56f95335b2bb763f79c3', '0001d65811200f762ee35d83a80b218b20674b44', '000c7e81e0c9c9582e0fd8164f0e88a41e9e406b', '00041d16f7ca613aef1ff969f4ea28dcf00786b0', '001528f82bf477d6bd00f49a284961ebec03afa4', '00085c989fd0eeadf3a90ef30a0f3365f63fcb13', '003b90bf2f7d242f29222f2f5d1f6aef5b3d134e', '0014ebc0748cdb7660ba7a8ffcf180857500acf7', '0093079a140a9517816cd676f07423649fed72df', '000208c4e6107bfd6cd71eac05a432dc0f2e2a2d', '000d0bd881c64cc9f5506be15c53c525f3307942', '0005ff6713782be27727414f35edfc0c3a935391', '001607ca3d340ee3c22c4aadf43f30c74c900499', '000c66881123d47c66d4fbac1790687219f217fd', '003bdf8ef1e3c4903fc3aa9784eab814a2ba640a', '001f290e26493b349c653d65c9a9a7cbac425507', '000472ac8f5f832cf3b224e9865d2479165f8028', '000d9051349bc45ba965f45a363de75eda538a32', '0008b250a8022f1b940ed7b3be9856ffc9e3e84e', '00187fea8945d11e573e0ec31b64353fc1835b5a', '000d94766d90a73ed3ff4227395c258841c417a0', '003dad1c7a1face3324a2247f71032efba5090e7', '0026cfb8c4ac7cfd134e855063017bbc6b5bf8c9', '00970b13dbaeae3cbff5e28bb96dd996e42502ef', '0005229a07ca377a3cc66855708d6bdec827be08', '000e012afbb8d8592b63fd82eaddc389da9f27ca', '0008c751fdfe18d2466060134eac971ca96950f6', '0018a6d238da56653f27749b8ad135aecca208c4', '0012c3fef3af880f4d9dfc7430057ebd91be1f05', '003df6a821e293a1a774bcb1cb2ff614225172af', '0035abaf2296edce783b7251492b4b6ef620f453', '0098ee882f3e562aa01a02d8cb72b25f051cba98', '0005c094c6149108dcc7a1d948aac284a5995b0b', '000f41d5eb2119c7f2733addeab2e099450e7015', '000a289d1dbad4990f34eecf3f80f0642c638f7e', '0019324ef18079266fb798f6a0de6895d417e5ce', '00167dc774047d3988380beb745db42de8057034', '003fa507e2d77eaaf801b3511b0b09fd4d91dea2', '00411891a8a74d20c92e4effb97b5ec8291389df', '00a0f41e541ac2887765bde3c29c7ec8b4c1678a', '0006e62ccef3867183349f0c648b22f371617e89', '0010ab72d752ccadecffacfd4f5df1f178f82041', '000a4a4e20bc8ebf28264dba55dacb3bc42cdd47', '001a5bcd6bfd4499813305e7410d0b6c25e6748a', '0016851584ce82537b14064e76b9f9fcc6f8debc', '0040335745d1c7480a840c6b66e4c14920fc51cb', '004aff4939b670ce233fb26a4bec86830adcdc2e', '00a66258087d038621f5b1931337613cad7e6ae8', '00075318a2bdcae6a26d9f98e6cee82c440cc621', '0010c03f2064f05a329f8d4f7d9e440e6f0e04bf', '000a87cdd8fd76199885473a99ba6d60cddd2f4d', '001b16ca6fda65ee41d050e019c0fda7979ec8b5', '001a04bd33986302d008d61480d66f9e20b816ce', '0046cff6a06e1d3bd1edd5e4a3d0ce0440a8ddf3', '004b88016f53fbd05e0b30970b4cdfffd79335f0', '00a6e08baea9e28320c01032aae787b6770c55a0', '000771cf42b0f60bbe607bfcfbc35bdd095176f3', '0011773f84280c354163b21ab89870c1fccf5b2c', '000c78b47cf7535486c46f822dcc5291d9e9694c', '001c36d4a80e4043aaa80c8ef55282d195177259', '001cc5c209e366b807c670753f130c5b43aa172a', '004d50c635dfe36825f395918edc28f428ed3ab8', '004f0a93aa367e697c428da14910cb76480fefff', '00a87e26a4b5cdc2cf5c12d4f745f637a2272346', '000777525d568efc76f8411bb90e7ca7158ac7cd', '00118fd3f0c3ccdf1caf5c0d6e26426ca458594b', '000ca5bac3fe63631c1399a053f1735261b1b109', '001e1e104b8cd6652e5f2ec1f3fe8554b0de9727', '001ffd26f7052263f94b5c896773426447244e00', '0050b799613716dafe408d5e2f32d6297bb2fb25', '0059b54f8e533811b9b82e17632175dd928fc350', '00b4aafdae34fb9d66434d509f84792c52c85047', '0008d0963ee791d7d0e753f23675196b0f2c1e09', '0011fc1ad5afd504661c32be307b793a1ee15271', '000d7253b344d609d4bc2daadd6d0d25840cca07', '001eeb23f3f9db78098440fd290fdc06bbc9c81b', '0020c7a0e3cf5cbccfc255f01117f8744a7365ae', '00512ffbc434a73924839866e4b76c1fcc55e2a8', '0059eca8fa1ef8ce6600e539dac8e3b261d08ebe', '00c1a2479d3e1b211abdc562106003bfc2e80e38', '000aa6539281e6a1015f06d18c1f0738af0451f0', '001249d166f05fe5d4e5cf3b8da280d82f73277d', '000dde2371f96b52dd58c9e84e225a8466bda609', '00219fc4fa38e33988c43b573de032c201643738', '0051ce3479f614b705256dcc71574b548d0b2df3', '005a43172e822844b0096276a4c5843b8977d503', '00c6d747d0e51b00c89ccb4ddf523aac60034db7', '000afdb88439e43d88567f5b2be758b46ff66357', '000f9738bed551936e2b8c29653b4c9aa5c2deef', '0022673c447fc7765acdb7a7f436b6682a4ecaca', '0067d1f2bcab4df2de71cd014d0ecf359b9b36e8', '0069f4e57f353ad3d1272fb6554d84e538e1b7fa', '00c7ed2a28b3cb758d1329b24c3adc81286d3e67', '006baca20f7f0088eecdb8f9b5d8a06dab36d8e0', '0013ab87b6398aa3d1739812dc124fbdf84ac901', '006d5e30468a1da5e85c0304fa0f316ec950ecab', '0061c985fdfdee46c9890866812584f4de6215fa', '00736852de78cbb107c3349fc7b06d04732d15e9', '0073c1b5cece8c9ede08fdc7a5c1b395ec94261a', '002c21149a2f3be8c0c8e5245cc805bde12ad74b', '00301f2935a3ad8a310400552f23304deb39a2fd', '007694d3d1b82773384c4105750751bb89995b39', '006a4a507967f0bc4646ea78b1f9f6357878f77e', '0033531abade346fa0f1bf2c7f17d06407ff1674', '00771b09e7beec75264e8921950ced3660dbbbd7', '0033a151692681c702fe17f1283c753d893d8484', '006c59a7d92cead2722b5071489d20ab77eed70b', '0033e6f310e65491a72d41e44a6f39c5b3ee8e87', '00779aa2cb14a5ea8611f19b1e96956ba78b3480', '00143f07b0688c5abd25d090c442239928a6f553', '00789efc18a553a9a6aeae9a2fbdf24ebb98f963', '007518e86f98a091eb78e216a8d2a72d896a28d0', '0077fbb8fd2d283307d11f83ae19be10c6502d28', '007f5787173256de0132f161b0ccf81e23904f14', '0080096b4869ef1a6cf81253cd5d4fb1b1e8d329', '0080619be03b5057c0cab2658bd8013841dce3c9', '00830cc046540dbfc3f3292299d6b82f3ab23f8c', '0079bc44c4972dd8c15852ecd51ac616e7687f49', '007abe24a7e0a7148d9954e2696ccdc590797338', '0086ef44accd26e7e436bb5724ca9e2b56fb4895', '0087ee8d6242cfe799b8021b48c5fe77d43ab83c', '0089fc02dd569dd27c9fccde0713a505cc2a94c0', '008c70a668fab7e9996a6b86ee00c7c2695ec3b5', '008d818a511d0024d5fc139bb2732e09671e0a13', '008fc21aca5b81aca87a72d6c4051d85e0f4e0d2', '00918097daaafe955877a272df221e0d6cef005e', '00164b45d488d61bf53c8f8096b1f965575261d8', '00169a6670f911a69391ffdbff2b7173586a9fa3', '0016cf2ca60931920ca8dd1e571202ef7bbb2cfe', '02400c7d6ab4638d27eddafd2bd37f567a5125b1', ]


completed_ids = []


def log_start_trace(num, i):
    with open('log1/process_{}.txt'.format(num), 'a') as fw:
        fw.write('{}\n'.format(i))

def log_invalid_id(num, i):
    with open('invalid_ids.txt', 'a') as fw:
        fw.write('{}:{}\n'.format(num, i))


def extract_features(feature_extractor, ids, num, cfg=None):
    count = 0
    print('started: process-{}'.format(num))
    for apk_id in tqdm(ids):
        if apk_id not in completed_ids:
            if apk_id not in invalid_ids:
                try:
                    log_start_trace(num, apk_id)
                    print('ing for: {}, process-{}'.format(apk_id, num))
                    ap = apkparser(os.path.join(feature_extractor.src, '{}'.format(apk_id)))
                    pcd = ap.get_pkg_class_dict()
                    for pkg in pcd:
                        fea1 = feature_extractor.get_package_fea(ap, pkg)
                        fea2 = feature_extractor.get_class_fea(ap, pkg)
                        fea3 = feature_extractor.get_method_fea(ap, pkg)
                    count += 1
                    print('completed: process-{}, {}/{}'.format(num, count, len(ids)+1))
             
                    #print('{}'.format(apk_id))
                    #print('{}\n'.format(pkg))
                    #print('{}'.format(np.hstack( (fea1,fea2,fea3) )))
                    #print('\n\n')
                except Exception as e:
                    log_invalid_id(num, apk_id)


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

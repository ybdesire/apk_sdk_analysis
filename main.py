import argparse
from feature_extractor import feature_extractor
import os


def extract_feature(apk_files_path, dst):
    samples_id_file = os.path.join( apk_files_path, 'samples_id.txt' )
    fe = feature_extractor( apk_files_path, dst, samples_id_file )
    fe.get_features()


if __name__=='__main__':
    arg_parser = argparse.ArgumentParser(description='APK package analysis tool')
    arg_parser.add_argument('act', help='action: extract or sth.')
    arg_parser.add_argument('-src', help='apk files folder path')
    arg_parser.add_argument('-dst', help='destination folder path for features output')
    args = arg_parser.parse_args()
    #print('args, a:{}, src:{}, dst:{}'.format(args.act, args.src, args.dst)) 
    if(args.act=='extract'):
        if(args.src==None or args.dst==None):
            print('please input the parameters of -src, and -dst')
        else:
            extract_feature(args.src, args.dst)

    








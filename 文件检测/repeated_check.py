import os
import hashlib
def get_file_library(path, file_dict):
    pathDir = os.listdir(path)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (path, allDir))
        if os.path.isfile(child):
            md5 = img_to_md5(child)
            # 将md5存入字典
            key = md5
            file_dict.setdefault(key, []).append(allDir)
            continue
        get_file_library(child, file_dict)
    

def img_to_md5(path):
    fd = open(path, 'rb')
    fmd5 = hashlib.md5(fd.read()).hexdigest()
    fd.close()
    return fmd5
    
def get_find_repeated_file(result_dic):
    
    for key, value in result_dic.items():
        if len(value) > 1:
            print('重复的md5',key)
            for obj in value:
                print('重复的文件',obj)
        
targetpath = '/Users/dxm/Library/Developer/Xcode/DerivedData/DemoProject-aiaukmoycnuiyaehpwiseekjqzye/Build/Products/Debug-iphoneos/DemoProject.app'
tinydict = {}
#保存结果
get_file_library(targetpath, tinydict)
#找到重复资源
get_find_repeated_file(tinydict)

#print('结果',tinydict)

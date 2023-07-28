import os

def findBigResources(path,threshold):
    pathDir = os.listdir(path)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (path, allDir))
        if os.path.isfile(child):
            # 获取读到的文件的后缀
            end = os.path.splitext(child)[-1]
            # 过滤掉dylib系统库和asset.car
            if end != ".dylib" and end != ".car":
                temp = os.path.getsize(child)
                # 转换单位：B -> KB
                fileLen = temp / 1024
                if fileLen > threshold:
                    #print(end)
                    print(child + " length is " + str(fileLen) + "kb");
        else:
            # 递归遍历子目录
            child = child + "/"
            findBigResources(child,threshold)

targetpath = '/Users/dxm/Library/Developer/Xcode/DerivedData/DemoProject-aiaukmoycnuiyaehpwiseekjqzye/Build/Products/Debug-iphoneos/DemoProject.app'
threshold = 20
findBigResources(targetpath, threshold)

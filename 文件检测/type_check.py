import os

def findTypeResources(path):
    pathDir = os.listdir(path)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (path, allDir))
        if os.path.isfile(child):
            # 获取读到的文件的后缀
            end = os.path.splitext(child)[-1]
            if end != ".dylib" and end != ".car" and end != ".png" and end != ".webp" and end != ".gif" and end != ".js" and end != ".css":
                print(child + " 后缀 " + end)
        else:
            # 递归遍历子目录
            child = child + "/"
            findTypeResources(child)
            
targetpath = '/Users/dxm/Library/Developer/Xcode/DerivedData/DemoProject-aiaukmoycnuiyaehpwiseekjqzye/Build/Products/Debug-iphoneos/DemoProject.app'
findTypeResources(targetpath)

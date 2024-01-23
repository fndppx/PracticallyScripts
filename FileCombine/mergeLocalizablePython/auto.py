# -*- coding:utf-8 -*-

import os
import time
from StringsFileUtil import StringsFileUtil
import shutil
def startConvert():
    print (os.getcwd())
 
    resourceDir = os.path.abspath(os.path.join(os.getcwd(), "../targetFiles/"))
    targetDir =  os.path.abspath(os.path.join(os.getcwd(), "../sourceFiles/"))
    
    print(resourceDir,targetDir)
    newAddStringsArr = []
    for a, dir, filenames in os.walk(targetDir):
        newAddStringsArr = [
                    fi for fi in filenames if fi.endswith(".strings")]
        # print("遍历内容:",a,strings,b)
    nameCodes = []
    for str in newAddStringsArr:
        code =  str.split(".")[0]
        if code == "zh_CN":
            code = "zh-Hans"
        if code == "zh_TW":
            code = "zh-Hant"
        if code == "pt_br":
            code = "pt-BR"
        if code == "in_ID":
            code = "id"
        nameCodes.append(code)
    
    print("nameCodes",nameCodes)

    # print("newAddStringsArrConten:",newAddStringsArr) 
    for _, dirnames, _ in os.walk(resourceDir):
        #获取到Resource目录下的所有.lproj文件夹
        lprojDirs = [di for di in dirnames if di.endswith(".lproj")]
        print("dirnames",dirnames)
        newAddedPath = ""
        for dirname in lprojDirs:
            print("dirname",dirname)
            orignalCode = dirname.split(".")[0]
            if orignalCode in nameCodes:
                code = orignalCode
                if code == "zh-Hans":
                   code = "zh_CN"
                if code == "zh-Hant":
                    code = "zh_TW"
                if code == "pt-BR":
                    code = "pt_br"
                if code == "id":
                    code = "in_ID"
                newAddedPath = targetDir + '/' + code + ".strings"
                
            else:
                print("notCorrectlyCode:",orignalCode)
                continue
            #遍历en.lproj文件夹下的所有内容,包含[InfoPlist.strings,Localizable.strings]
            for _, _, filenames in os.walk(resourceDir+'/'+dirname):
                #取出所有的.strings
                stringsFiles = [
                    fi for fi in filenames if fi.endswith("Localizable.strings")]
                print("filenames",filenames)
                for stringfile in stringsFiles:
                    path = resourceDir+'/'+dirname+'/' + stringfile
                    print("path:",path)
                    print("stringfile",stringfile)
                    (keys, values,desc) = StringsFileUtil.getKeysAndValues(
                        path)
                    (keys2, values2, desc2) = StringsFileUtil.getKeysAndValues(
                        newAddedPath)
                    
                    for index in range(len(keys2)):
                        key = keys2[index]
                        if key in keys:
                            keyIndex = keys.index(key)
                            values[keyIndex] = values2[index]
                            desc[keyIndex] = desc2[index]
                        else:
                            keys.append(key)
                            values.append(values2[index])
                    
                    os.remove(path)
                    iosFileManager = open(path, "wb")
                    print("iosStringsOutputPath",path)
                    content = ""
                    for index in range(len(keys)):
                        key = keys[index]
                        value = values[index]
                        des = desc[index]
                        content = content + "\"" + key + "\"" + \
                        "=" + "\"" + value + "\";"+ des + "\n"
                       
                    iosFileManager.write(content.encode("utf-8"))
                  
                    iosFileManager.close()
       
                    

          

def main():
    startConvert()


main()

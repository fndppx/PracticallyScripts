# -*- coding: utf-8 -*
import os
import os.path
import codecs
import xml.dom.minidom
import re
import datetime
import fileinput
import string
import zipfile

def dfs_get_zip_file(input_path,result):
    
#
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path+'/'+file):
            dfs_get_zip_file(input_path+'/'+file,result)
        else:
            result.append(input_path+'/'+file)

def zip_path(input_path,output_path,output_name):

    f = zipfile.ZipFile(output_path+'/'+output_name,'w',zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path,filelists)
    for file in filelists:
        f.write(file)
    f.close()
    return output_path+r"/"+output_name

#备份
def bak():
    meragefiledir = os.getcwd() #当前Python文件目录
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y%m%d%H%M%S")
    bakFile(meragefiledir+'/targetFiles', meragefiledir+'/bak_targetFiles'+otherStyleTime)
    zip(meragefiledir+'/targetFiles', 'bak_targetFiles'+otherStyleTime)
    pass

def bakFile(fromPath, toPath):
    #print('cp -r '+fromPath+' '+toPath)
    os.system('cp -r '+fromPath+' '+toPath)
    pass

# 添加版本标记
def addTag(targetFilePath, tag):
    print('添加版本标记:'+tag)
    count = len(open(targetFilePath,'r').readlines()) #行数
    for line in fileinput.input(targetFilePath,inplace = True):
        # 在指定行后添加一行
        if fileinput.lineno() == count:
            print(line.rstrip())
            print(tag)
        else:
            print(line.rstrip())
        pass

#合并文件
def merage(sourceFilePath, targetFilePath):
    # 添加标记
    # addTag(targetFilePath, '\n//TEST\n')
    addTag(targetFilePath, '')
    # 合并
#    os.system('cat '+sourceFilePath+' >> '+targetFilePath)

    #合并替换
    update_file(targetFilePath,sourceFilePath)
    pass
    
#替换合并文件
def update_file(file1_path, file2_path):
    # 读取file2.txt的内容
    with open(file2_path, 'r', encoding='utf-8') as file2:
        updates = dict(re.findall(r'(\S+)="([^"]*)";', file2.read()))

    # 读取file1.txt的内容并更新
    with open(file1_path, 'r', encoding='utf-8') as file1:
        content = file1.read()

    # 替换file1.txt中的对应内容或追加
    for key, value in updates.items():
        pattern = re.compile(rf'({re.escape(key)}=")([^"]*)(";)')
        if pattern.search(content):
            content = re.sub(pattern, rf'\g<1>{value}\g<3>', content)
        else:
            content += f'\n{key}="{value}";'

    # 将更新后的内容写回file1.txt
    with open(file1_path, 'w', encoding='utf-8') as file1:
        file1.write(content)
        
    pass
    
#根据语言类型合并
def merageLanguage(language):
    meragefiledir = os.getcwd() #当前Python文件目录
    # sourceFilePath
    sourceFilePath = meragefiledir+"/sourceFiles/"+language+".strings"
    # targetFilePath
    targetFilePath = meragefiledir+"/targetFiles/"+language+".lproj/InfoPlist.strings"
    # if (os.path.exists(sourceFilePath) & os.path.exists(targetFilePath)) :
    if (os.path.isfile(sourceFilePath) & os.path.isfile(targetFilePath)) :
        print(language)
        merage(sourceFilePath, targetFilePath)
    else :
        print(language + ': File is not exists')
    pass

#根据数组遍历
def walkDir(languageList):
    for lang in languageList:
        merageLanguage(lang)
        pass
    pass

#更改文件名
def changeFileExtentionName(fileName):
    if str.find(fileName, 'in_ID')!=-1:
        os.rename(fileName,fileName.replace('in_ID','id'))
        
    if str.find(fileName, 'pt_br')!=-1:
        os.rename(fileName,fileName.replace('pt_br','pt-BR'))

    if str.find(fileName, 'zh_CN')!=-1:
        os.rename(fileName,fileName.replace('zh_CN','zh-Hans'))
        
    if str.find(fileName, 'zh_TW')!=-1:
        os.rename(fileName,fileName.replace('zh_TW','zh-Hant'))
        
    pass

#遍历文件夹下的所有文件
def gci(filepath):
    #遍历filepath下所有文件，包括子目录
  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)            
    if os.path.isdir(fi_d):
        gci(fi_d)
    else:
        changeFileExtentionName(fi_d)
        # print(fi_d)
        pass

#遍历
def verifyStrList(stringList, languageList):
    for language in languageList:
        verifyList(stringList, language, True)
    # verifyList(stringList, 'en')
    pass

def verifyList(stringList, language, isLocalFilePath):
    if isLocalFilePath==True:
        sourceFilePath = meragefiledir+"/targetFiles/"+language+".lproj/Localizable.strings"
    else:
        sourceFilePath = meragefiledir+"/sourceFiles/"+language+".strings"
    
    if (os.path.isfile(sourceFilePath)) :
        lackList = []
        for key in stringList:
            flag = False
            file = open(sourceFilePath)
            for line in file:
                if str.find(line, '\"'+key+'\"=')!=-1:
                    flag = 1
            
            if flag==False:
                lackList.append(key)
            elif flag==True:
                pass
                # print('have: '+key)
            file.close()
        if len(lackList)>0:
            print('\n'+language)
            print('lack:')
            print(lackList)
            pass
        
    else :
        print(language + ': File is not exists')
    pass

########## Main ##########

lst30 = ['ar','bg','cs','da','de','el','en','es','fa','fr','hi','hr','hu','id','it','ja','ko','nl','pl','pt','ro','ru','sk','sr','sv','tr','uk','vi','zh-Hans','zh-Hant']

lst18 = ['ar','de','en','es','fa','fr','id','it','ja','ko','nl','pl','pt-BR','ru','tr','zh-Hans','zh-Hant']
lst18 = ['pt-BR']
#lst18 = ['id','zh-Hans','zh-Hant','ko','nl']


#lst24 = ['ar','cs','da','de','en','es','fa','fi','fr','id','it','ja','ko','nb','nl','pl','pt-BR','pt-PT','ru','sv','tr','uk','zh-Hans','zh-Hant']
#获取目标文件夹的路径  
# merageLanguage('en')

#改名
meragefiledir = os.getcwd() #当前Python文件目录
gci(meragefiledir)

#验证
stringList18 = ['action_reset',
] 

stringList30 = []

# verifyStrList(stringList18, lst18)
# verifyStrList(stringList30, lst30)

#备份
# bak()

#替换
walkDir(lst18)






# for line in fileinput.input():  
#     line = re.sub(r'\* ', r'<h2 id="\2">\1</h2>', line.rstrip())  
#     print(line)  

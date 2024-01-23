#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from Log import Log
import codecs
import re
import io


def removeComments(s):
    for x in re.findall(r'("[^\n]*"(?!\\))|(//[^\n]*$|/(?!\\)\*[\s\S]*?\*(?!\\)/)', s, 8):
        print("xxxxxxxx:",x)
        s = s.replace(x[1], '')
    return s


class StringsFileUtil:
    'iOS Localizable.strings file util'

    @staticmethod
    def writeToFile(keys, values, directory, name, additional):
        if not os.path.exists(directory):
            os.makedirs(directory)

        Log.info("Creating iOS file:" + directory + name)

        fo = open(directory + "/" + name, "wb")

        for x in range(len(keys)):
            if values[x] is None or values[x] == '':
                Log.error("Key:" + keys[x] +
                          "\'s value is None. Index:" + str(x + 1))
                continue

            key = keys[x].strip()
            value = values[x]
            content = "\"" + key + "\" " + "= " + "\"" + value + "\";\n"
            fo.write(content)

        if additional is not None:
            fo.write(additional)

        fo.close()

    @staticmethod
    def getKeysAndValues(path):
        print("getKeysAndValues1111111")
        if path is None:
            Log.error('file path is None')
            return

        # 1.Read localizable.strings
        encodings = ['utf-8', 'utf-16']
        for e in encodings:
            try:
                file = codecs.open(path, 'r', encoding=e)
                string = file.read()
                file.close()
            except UnicodeDecodeError:
                print('got unicode error with %s , trying different encoding' % e)
            else:
                break

        # 2.Remove comments
        print("originalComments:",string)
        # string = removeComments(string)
        #
        keys = []
        values = []
        desc = []
        arr = string.split('\n')
        for str in arr :
            arr1 = str.split(';')
            if len(arr1)> 0:
                str1 = arr1[0]
                if len(arr1) >1:
                    desc.append(arr1[1])
                else:
                    desc.append("")
                arr2 = str1.split('=')
                if len(arr2) == 2:
                    key = arr2[0]
                    value = arr2[1]
                    # print("keyValue:",key,value)
                    keys.append(key[1:-1])
                    values.append(value[1:-1])

        print("desc:",desc)
        # 3.Split by ";
        # localStringList = string.split('\";')
        # list = [x.split('=') for x in localStringList]
        # #对二维列表进行排序
        # list = sorted(list,key=(lambda x:x[0]))
        # print("list:",list)
        # # 4.Get keys & values
        # keys = []
        # values = []
        # for x in range(len(list)):
        #     keyValue = list[x]
          
        #     if len(keyValue) > 1:
        #         arr = keyValue[0].split('\"')
        #         key = arr[1]
        #         print("arr11111:",keyValue)
        #         value = keyValue[1][1:]
        #         keys.append(key)
        #         values.append(value)

        return (keys, values, desc)

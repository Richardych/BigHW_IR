# coding=utf-8
import os
import re

class Singlestringcomp:
    def __init__(self):
        return
    
    # 写入磁盘前先进行单一字符串压缩
    @staticmethod
    def sscompress(sorted_dic):
        """
        sorted_dic: [('an',1), ('you',1), ('me',1) ...]
        dic_sscomp: 2an3you2me...        
        """
        tmp = ''
        for k in sorted_dic:
            tmp += str(len(k))
            tmp += k
        return tmp
        
    # 把压缩后的词典写入磁盘
    @staticmethod
    def write_dic(sorted_dic, file_path):
        dic_sscomp = Singlestringcomp.sscompress(sorted_dic)
        with open(file_path, 'w') as f:
            f.writelines(dic_sscomp)

    # 从压缩的词典中恢复出原词典
    @staticmethod
    def read_dic(file_path):
        with open(file_path, 'r') as f:
            dic_sscomp = f.readline()
        return Singlestringcomp.ssdecompress(dic_sscomp)


    # 从压缩的词典中解压出原词项
    @staticmethod
    def ssdecompress(dic_sscomp):
        term_dic = []
        term_dic = re.findall(r'[a-z]+', str(dic_sscomp))
        return term_dic

if __name__ == '__main__':
    pass

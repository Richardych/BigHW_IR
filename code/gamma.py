# coding=utf-8

import struct

class Gamma:
    def __init__(self):
        return

    # 把未经gamma压缩的倒排记录表写入磁盘
    @staticmethod
    def write_invert_index_noencode(inverted_index, file_path):
        """
        inverted_index: [[1,2,3],[1],[1],...]
        file_path: BigHW_IR/data/indexer_block/*_invindex
        """
        with open(file_path, 'w') as f:
            for i in inverted_index:
                for j in range(len(i)):
                    if j != range(len(i))[-1]:
                        f.write(str(i[j]))
                        f.write(' ')
                    else:
                        f.write(str(i[j]))
                f.write('\n')
    
    # gamma 对单个docID编码
    @staticmethod
    def gamma_encode(num):
        """ num>0 """
        bin_tmp = ''
        i = 0
        """ 
        因为1: 0,增量编码时可能出现 00000000,这样解码时无法确定边界！
        为了确定编解码时的边界问题，使所有id都+1,解码后-1 
        """
        num = num + 1
        while num > 0:
            mod = num % 2
            bin_tmp = str(mod) + bin_tmp
            num = num / 2
        lens_one = ''
        offset = bin_tmp[1:]
        lens = len(offset)
        for i in range(lens):
            lens_one += '1'
        lens_one += '0'
        res = lens_one + offset
        return res
    
    # gamma 对单个docID解码
    @staticmethod
    def gamma_decode(code):
        code_len = len(code)
        i = 0
        res = 0
        while code[i] == '1':
            i += 1
        res = 1<<i
        while i>0:
            x = code_len - i
            i -= 1
            if code[x] == '1':
                res |= (1<<i)
            else:
                pass
        return res - 1
    
    # 对gamma编码的所有词项的docID列表 进行解码
    @staticmethod
    def entity_gamma_decode(index_encode):
        """
        注意: index_encode第一个很长很长的字符串，结尾为0,每个词项的docID列表串之间为0
        ret:  返回词项term对应的每个docID
        """
        ret = []
        tmp_ret = []
        i = 0
        idoffset_len = 0
        pre_idnum = 0
        while i < len(index_encode):
            if index_encode[i] == '0':
                """ 这个词项的所有ID已经装完 """
                if len(tmp_ret) != 0:
                    ret.append(tmp_ret)
                    """ 准备装下一个词项的ID """
                    i += 1
                    tmp_ret = []
                    pre_idnum = 0
                else:
                    return ret
            """ 判断id偏移量长度 """
            while index_encode[i+idoffset_len] == '1':
                idoffset_len += 1
            """ 如果存在继续的id """
            if idoffset_len > 0:
                idnum = Gamma.gamma_decode(index_encode[i:i+1+idoffset_len*2])
                tmp_ret.append(idnum+pre_idnum)
                pre_idnum += idnum
            i += 1+idoffset_len*2
            idoffset_len = 0
        return ret

    # gamma 对一个词项的docID列表 编码
    @staticmethod
    def entity_gamma_encode(inverted_index):
        """
        inverted_index: [[1,12,30],[1,2],[15]..]
        """
        res = []
        for id_lst in inverted_index:
            tmp = Gamma.gamma_encode(id_lst[0])
            i = 0
            for j in id_lst[1:]:
                """ 对差值进行编码 """
                tmp += Gamma.gamma_encode(j-id_lst[i])
                i += 1
            res.append(tmp)
        return res

    # 把gamma编码的倒排记录表写入磁盘
    @staticmethod
    def write_invert_index_encode(inverted_index, file_path):
        """
        inverted_index_encode: ['11000','1110101',...]
        """
        with open(file_path, 'wb') as f:
            """ 对合并的全局倒排记录表进行gamma编码 """
            inverted_index_encode = Gamma.entity_gamma_encode(inverted_index)
            temp = k = 0
            """ 以四个bit(int)为单位，一次性写完 """
            for row in inverted_index_encode:
                """ 遍历每一个term对应的所有docID经gamma压缩后形成的字符串 """
                for x in row:
                    temp |= (1 << k) if x == '1' else 0
                    k += 1
                    """ i : int, 32 bit """
                    if k == 31:
                        f.write(struct.pack('i', temp))
                        temp = k = 0
                k += 1
                if k == 31:
                    f.write(struct.pack('i', temp))
                    temp = k = 0
            if k != 0:
                f.write(struct.pack('i', temp))
            f.write(struct.pack('i', 0))

    # 把gamma编码并压缩的全局倒排记录表 解压并解码，恢复倒排记录表
    @staticmethod
    def read_invert_index_decode(file_path):
        with open(file_path, 'rb') as f:
            """ 以四字节为单位，一次性读完 """
            longencodestr = ''
            while True:
                tmp_32bit = f.read(4)
                inverted_index_encode = struct.unpack('i', tmp_32bit)[0]
                if inverted_index_encode is 0:
                    """ 读到最后一位 """
                    break
                i = 0
                while i < 31:
                    longencodestr += '1' if inverted_index_encode  & (1<<i) else '0'
                    i += 1
        return Gamma.entity_gamma_decode(longencodestr)

if __name__ == '__main__':
    pass

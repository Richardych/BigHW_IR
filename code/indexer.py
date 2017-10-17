# coding=utf-8
import os
from tokenstream import TokenStream

class indexer:
    def __init__(self, data_path, max_block=10000):
        self.dir_path = os.path.dirname(data_path)
        self.block_dir = os.path.join(data_path, 'indexer_block')
        self.block_path_repo = []
        self.max_block = max_block
        """ 判断词项流是否为空 """
        self.empty_stream = False
        """分词"""
        self.tokenstream = TokenStream(data_path)



    # SPIMI算法构建索引块
    def spimi_invert(self):
        term_dic = {}
        """ 倒排索引 """
        inverted_index = []
        """ 记录词项在倒排记录表位置，不排序 """
        term_cnt = 0
        block_size = 0
        """ 每一个block维护一个字典和倒排记录表 """
        while block_size < self.max_block:
            tmp_term_pos_docid = self.tokenstream.get_next_term_pos_docid()
            if tmp_term_pos_docid is None:
                self.empty_stream = True
                break
            """ 返回不是None """
            term,term_pos,docid = tmp_term_pos_docid
            """ 不在词典中，加入并返回在词典中的位置 """
            if term not in term_dic:
                term_dic[term] = term_cnt
                inverted_index.append([docid])
                term_cnt += 1
            else:
                """ 返回在词典中位置 """
                pos = term_dic[term]
                """ 词项所在文档ID不在倒排记录表里 """
                if docid != inverted_index[pos][-1]
                    inverted_index[pos].append(docid)
            block_size += 1
        return term_dic, term_cnt, inverted_index

    # 索引块持久化
    def write_index_block(self, block_path):



    # 构建索引块
    def build_index_block(self):
        index_block = 0
        while True:
            """ 用SPIMI算法构建索引块 """
            if self.empty_stream == True:
                break
            term_dic, term_cnt, inverted_index = self.spimi_invert()
            index_block += 1
            self.block_path_repo.append(os.path.join(self.block_dir, 
                'index_block_' + str(indexer_block)))
            """ 索引块持久化 """
            

    # 构建倒排记录表和词典
    def build_indexer:
        """
        1.构建索引块,合并索引块,写入磁盘过程中压缩
        2.对每一个块产生独立的字典，和倒排索引
        3.对倒排记录表不需要排序
        """
        # 构建索引块
        self.build_index_block()

if __name__ == '__main__':
    pass











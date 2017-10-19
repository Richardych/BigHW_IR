# coding=utf-8
import bs4
import os
import re

class TokenStream:
    def __init__(self, data_dir):
        """ 读取文档，得到倒排记录表term - docid """
        self.file_dir = data_dir
        self.file_names = os.listdir(self.file_dir)
        self.document = None
        self.documentid = 0
        self.document_term = []
        self.document_num = {}
        self.termpos = -1

        #self.term_cnt = 0
        #self.doc_cnt = 0

    def cal_term_doc(self):
        """
        """
        pass 

    # 得到文档词条里的词项
    def get_term_from_doc(self, token):
        term = []
        for i,word in enumerate(token):
            term.append((word,i))
        return term
    
    # 获得语料库下一个文件路径
    def get_next_file_path(self):
        if len(self.file_names) is 0:
            return None
        file_path = os.path.join(self.file_dir, self.file_names[0])
        self.file_names.pop(0)
        return file_path

    # 获得下一篇文档 和 对应的词项
    def next_doc_and_term(self):
        """
        从file_dir下读取一篇文档
        self.document 的读取是doc, '\n', doc, '\n' ...
        """
        if type(self.document) is bs4.element.Tag:
            self.document = self.document.next_sibling
        while type(self.document) is not bs4.element.Tag:
            if self.document is None:
                file_path = self.get_next_file_path()
                """ 语料库里的文档被读取完 """
                if file_path is None:
                    #return None
                    break
                with open(file_path, 'r') as doc_file:
                    soup = bs4.BeautifulSoup(doc_file, features = 'lxml')
                self.document = soup.doc
            else:
                self.document = self.document.next_sibling

        """ 获得self.document 里的词项, 放在document_term """
        if self.document is None:
            self.document_term = None
            return None
        else:
            self.documentid += 1
            docno_name = self.document.docno.string
            """ 将 文档ID - 文档名 存到一个字典 """
            self.document_num[self.documentid] = docno_name
            """ 每一个文档转成 字符串 """
            temp = ''
            """ 把文档转成词条 """
            for row in self.document.docno.next_siblings:
                if type(row) is bs4.element.Tag:
                    row = row.strings
                if type(row) is not bs4.element.NavigableString:
                    continue
                temp += row.lower().encode('utf-8')
            """
            接下来 获得词项 term
            对每一篇文档，词项位置置-1
            """
            self.termpos = -1
            self.document_term = self.get_term_from_doc(re.findall(r'\w+', temp))

    # 去读下一个词项
    def get_next_term(self):
        """ 用来判断一篇文档的词是否读完 """
        self.termpos += 1 
        """
        如果词项位置超过了一篇文档数,读完
        """
        while self.termpos >= len(self.document_term):
            self.next_doc_and_term()
            self.termpos += 1
            if self.document_term is None:
                return None
        return self.document_term[self.termpos]
    
    # 获得下一个词项的词项，词项位置，文档id，
    def get_next_term_pos_docid(self):
        tmp_term_pos = self.get_next_term()
        if tmp_term_pos is None:
            return None
        return (tmp_term_pos[0],tmp_term_pos[1],self.documentid)
    
       
    

if __name__ == '__main__':
    dd = TokenStream('/home/superhui/Informationretrieval/IR/BigHW_IR/data/doc')
    #dd.next_doc_and_term()
    #print dd.document
    #print dd.get_next_term()
    #print dd.get_next_term()
    #for i in range(10000):
    #    print dd.get_next_term_pos_docid()

# coding=utf-8

class Find():
    def __init__(self, dic, inverted_index, doc_num):
        self.dic = dic
        self.inverted_index = inverted_index
        self.doc_num = doc_num
        self.dic_dic = {}
        for i,term in enumerate(self.dic):
            self.dic_dic[term] = i

    # 返回词项倒排记录表, [1,2,3,4]
    def exe_search(self, term):
        if term in self.dic:
            return self.inverted_index[self.dic_dic[term]]
        else:
            return []

    # 查询主函数，返回关键字的倒排记录表
    def find(self, qinfo):
        qinfo = qinfo.strip(' ')
        qterms = qinfo.split(' ')
        for i in qterms:
            if i == '':
                qterms.remove(i)
        if len(qterms) == 0:
            return None
        logic_op = ''
        tmp_res_lst = []
        for i,term in enumerate(qterms):
            if (i != 0) and (term == '&' or term  == '|'):
                logic_op = term
                continue
                #qterms.remove(i)
            if logic_op == '':
                tmp_res_lst = self.exe_search(term)
            else:
                tmp = self.exe_search(term)
                if logic_op == '|':
                    if len(tmp) != 0:
                        for k in tmp:
                            if k not in tmp_res_lst:
                                tmp_res_lst.append(k)

                if logic_op == '&':
                    common = []
                    if len(tmp) != 0:
                        for j in tmp_res_lst:
                            if j in tmp:
                                common.append(j)
                        tmp_res_lst = common
                    else:
                        tmp_res_lst = []
                logic_op = ''
        return tmp_res_lst

    def show_result(self, tmp_res_lst):
        if len(tmp_res_lst) == 0:
            print "Sorry! can't find nothing!"
        else:
            print '\t','doc_id','  ','doc_title'
            for doc_id in tmp_res_lst:
                print '\t',doc_id,':  ',self.doc_num[doc_id]

if __name__ == '__main__':
    pass











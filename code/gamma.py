# coding=utf-8

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

if __name__ == '__main__':
    inin = [[1,2,3],[1,2],[1,2,3,4]]
    Gamma.write_invert_index_noencode(inin,'./yydoc')



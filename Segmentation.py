import re
import Reader
import copy
#分割单词
def SplitCluster(result):
    """
    将单词按照分隔符进行分割
    :param result:聚类结果
    :return: 单词分割后的聚类结果
    """
    result_split = result[:]
    for i in range(len(result)):
        for j in range(len(result[i])):
            tmp = re.split(' |\:|\;|\=', str(result[i][j]).strip('[').strip(']'))
            result_split[i][j]= tmp[:]

    #去掉无意义的''字符
    result_split_tmp = copy.deepcopy(result_split)
    for i in range(len(result_split_tmp)):
        for j in range(len(result_split_tmp[i])):
            for k in range(len(result_split_tmp[i][j])):
                if result_split_tmp[i][j][k] == '' or result_split_tmp[i][j][k] =="'":
                    result_split[i][j].remove(result_split_tmp[i][j][k])
    return result_split

if __name__ == '__main__':
    result = Reader.readfile('result38.bin')
    result_split = SplitCluster(result)
    for i in range(len(result_split)):
        print(result_split[i])
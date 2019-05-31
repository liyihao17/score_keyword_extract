import Reader
import Segmentation
import ClassFile
import copy

def DeleteRepetition(result_split):
    """
    去掉重复的分词,并且每一聚类的类别为一行
    :param result_split: 分词后的结果
    :return: 去掉重复后的分词结果
    """
    delete_result = []
    result_split_tmp = copy.deepcopy(result_split)
    for i in range(len(result_split)):
        tmp = []
        for j in range(len(result_split[i])):
            for k in range(len(result_split[i][j])):
                if result_split[i][j][k] not in tmp:
                    tmp.append(result_split[i][j][k])
        delete_result.append(tmp)
    return delete_result

def BuildClass(delete_result):
    """
    将去重后的结果每一个词语都构建一个类
    :param delete_result: 去重后的单词
    :return: 构建的类的列表,列表是二维的,第一维说明其在哪个类别中
    """
    candidate = copy.deepcopy(delete_result)
    for i in range(len(delete_result)):
        for j in range(len(delete_result[i])):
           candidate[i][j] = ClassFile.candidate(cluster=i,word=delete_result[i][j])
    return candidate

def CalLenScore(candidate,stdmin,stdmax):
    """
    计算长度分数,定义长度分数为减去标准长度加一然后倒数
    :param candidate:候选词对象列表
    :param stdmin:标准最小长度
    :param stdmax:标准最大长度
    """
    for i in range(len(candidate)):
        for j in range(len(candidate[i])):
            if len(candidate[i][j].word) <= stdmax and len(candidate[i][j].word) >= stdmin:
                candidate[i][j].SetLenScore(1)
            elif len(candidate[i][j].word) < stdmin:
                len_score = 1/(stdmin - len(candidate[i][j].word)+1)
                candidate[i][j].SetLenScore(len_score)
            elif len(candidate[i][j].word) > stdmax:
                len_score = 1/(len(candidate[i][j].word) - stdmax+1)
                candidate[i][j].SetLenScore(len_score)

def CalSupScore(candidate,result_split):
    """
    计算每一个候选词的分数,并写到每个候选词对象中
    :param candidate: 候选词对象列表
    :param result_split: 分词后的结果
    """
    for i in range(len(candidate)):
        for j in range(len(candidate[i])):
            count = 0
            for k in range(len(result_split[i])):
                if candidate[i][j].word in result_split[i][k]:
                    count = count + 1
            candidate[i][j].SetSupScore(count/len(result_split[i]))

def CalPosScore(candidate,result_split):
    """
    计算每个关键词的位置分数
    :param candidate: 候选词对象列表
    :param result_split: 分词结果
    """
    for i in range(len(candidate)):
        for j in range(len(candidate[i])):
            flag = 0
            for k in range(len(result_split[i])):
                if candidate[i][j].word in result_split[i][k] and flag == 0:
                    min_index = max_index = result_split[i][k].index(candidate[i][j].word)
                    flag = 1
                if candidate[i][j].word in result_split[i][k] and flag == 1:
                    index = result_split[i][k].index(candidate[i][j].word)
                    if index < min_index:
                        min_index = index
                    if index > max_index:
                        max_index = index
            sub = max_index - min_index
            if sub == 0:
                pos_score = 1
            else:
                pos_score = 1/(sub+1)
            candidate[i][j].SetPosScore(pos_score)

    for i in range(len(candidate)):
        for j in range(len(candidate[i])):
            count = 0
            for k in range(len(result_split[i])):
                if candidate[i][j].word in result_split[i][k]:
                    count = count + 1
                if count >=2:
                    break
            if count == 1:
                candidate[i][j].SetPosScore(0)

def GenCandidateList(candidate):
    """
    生成候选词列表,后面带着候选词的总分数
    :param candidate: 候选词对象列表
    :return: 候选词-分数列表
    """
    candidate_list = []
    for i in range(len(candidate)):
        tmp = []
        for j in range(len(candidate[i])):
            tmp.append([candidate[i][j].word,candidate[i][j].score])
        candidate_list.append(tmp)
    return candidate_list

def TakeLast(elem):
    """
    用于排序函数,获取最后一个元素,在排序的时候可以按最后一个元素进行排序
    :param elem: 列表
    :return: 列表中最后一个元素
    """
    return elem[-1]

def CandidateListSort(candidate_list):
    """
    对所有候选关键词按照分数进行排序
    :param candidate_list: 候选词-分数列表
    :return: 按照分数排序的候选词-分数列表
    """
    candidate_list_tmp = copy.deepcopy(candidate_list)
    for i in range(len(candidate_list_tmp)):
        candidate_list_tmp[i].sort(key=TakeLast,reverse=True)
        sorted_candidate_list = copy.deepcopy(candidate_list_tmp)
    return sorted_candidate_list

def CutByRank(sorted_candidate_list,proportion):
    """
    通过所占聚类类别中的比例提取排名靠前的关键词
    :param sorted_candidate_list: 已经排序好的关键词列表
    :param proportion: 比例
    :return: 按照比例提取的关键词
    """
    extracted_word = []
    for i in range(len(sorted_candidate_list)):
        lenth = int(len(sorted_candidate_list[i]) * proportion)
        tmp = []
        limit_score = sorted_candidate_list[i][lenth][1]
        j = 0
        while j < len(sorted_candidate_list[i]) and sorted_candidate_list[i][j][1] >= limit_score:
            tmp.append(sorted_candidate_list[i][j])
            j = j + 1
        extracted_word.append(tmp)
    return extracted_word

def CutByScore(sorted_candidate_list,score_limit):
    """
    通过各类分数进行关键词提取
    :param sorted_candidate_list: 已经排序好的关键词列表
    :param score_limit: 分数
    :return: 按照分数提取的关键词
    """
    extracted_word = []
    for i in range(len(sorted_candidate_list)):
        tmp = []
        for j in range(len(sorted_candidate_list[i])):
            if sorted_candidate_list[i][j][1] >= score_limit:
                tmp.append(sorted_candidate_list[i][j])
            else:
                break
        extracted_word.append(tmp)
    return extracted_word

def CutByRankAndScore(sorted_candidate_list,proportion,score_limit):
    """
    过滤满足排名和分数的关键词
    :param sorted_candidate_list: 已经排序好的关键词列表
    :param proportion: 比例
    :param score_limit: 分数
    :return: 按照排名和分数提取的关键词
    """
    extracted_word_tmp = []
    for i in range(len(sorted_candidate_list)):
        lenth = int(len(sorted_candidate_list[i]) * proportion)
        tmp = []
        limit_score = sorted_candidate_list[i][lenth][1]
        j = 0
        while j < len(sorted_candidate_list[i]) and sorted_candidate_list[i][j][1] >= limit_score:
            tmp.append(sorted_candidate_list[i][j])
            j = j + 1
        extracted_word_tmp.append(tmp)

    extracted_word = copy.deepcopy(extracted_word_tmp)
    for i in range(len(extracted_word_tmp)):
        for j in range(len(extracted_word_tmp[i])):
            if extracted_word_tmp[i][j][1] < score_limit:
                extracted_word.remove(extracted_word_tmp[i][j])
    return extracted_word

def ExtractedWordDeleteRepetition(extracted_word):
    """
    得出每个聚类去重后的所有关键词
    :param extracted_word: 未去重的每个聚类类别内部的关键词
    :return: 去重后提取的关键词
    """
    extracted_result = []
    for i in range(len(extracted_word)):
        for j in range(len(extracted_word[i])):
            if extracted_word[i][j][0] not in extracted_result:
                extracted_result.append(extracted_word[i][j][0])
    return extracted_result

if __name__ == '__main__':
    result = Reader.readfile('result38.bin')
    result_split = Segmentation.SplitCluster(result)
    delete_result = DeleteRepetition(result_split)
    candidate = BuildClass(delete_result)
    CalLenScore(candidate,2,15)
    CalSupScore(candidate,result_split)
    CalPosScore(candidate,result_split)
    for i in range(len(candidate)):
        for j in range(len(candidate[i])):
            candidate[i][j].CalScore()
    candidate_list = GenCandidateList(candidate)
    sorted_candidate_list = CandidateListSort(candidate_list)

    for i in range(len(sorted_candidate_list)):
        print("")
        for j in range(len(sorted_candidate_list[i])):
            print(sorted_candidate_list[i][j])

    extracted_word = CutByRank(sorted_candidate_list,0.15)
    print("the result of cut by rank: ")
    for i in range(len(extracted_word)):
        print("")
        for j in range(len(extracted_word[i])):
            print(extracted_word[i][j])

    extracted_word = CutByScore(sorted_candidate_list,2.0)
    print("the result of cut by score: ")
    for i in range(len(extracted_word)):
        print("")
        for j in range(len(extracted_word[i])):
            print(extracted_word[i][j])
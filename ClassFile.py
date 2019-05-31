class candidate(object):
    def __init__(self,cluster,word):
        """
        候选词有六个基本属性
        :param cluster: 聚类中的所在类
        :param word:单词
        :param len_score:长度分数
        :param pos_score:位置分数
        :param sup_score:支持度分数
        :param score:总分数
        """
        self.cluster = cluster
        self.word = word
        self.len_score = 0
        self.pos_score = 0
        self.sup_score = 0
        self.score = 0

    def SetLenScore(self,len_score):
        self.len_score = len_score
    def SetPosScore(self,pos_score):
        self.pos_score = pos_score
    def SetSupScore(self,sup_score):
        self.sup_score = sup_score
    def CalScore(self):
        self.score = self.len_score + self.pos_score + self.sup_score
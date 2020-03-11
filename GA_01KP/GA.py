# -*- coding: utf-8 -*-

import random
from Life import Life


class GA(object):
    """遗传算法类"""

    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun=lambda life: 1):
        self.croessRate = aCrossRate              # 交叉概率
        self.mutationRate = aMutationRage         # 突变率
        self.lifeCount = aLifeCount               # 种群大小
        self.geneLenght = aGeneLenght             # 染色体长度(城市个数)
        self.matchFun = aMatchFun                 # 适值函数
        self.lives = []                           # 种群
        self.best = None                          # 保存这一代中最好的个体
        self.generation = 1                       # 迭代次数
        self.crossCount = 0                       # 交叉个数
        self.mutationCount = 0                    # 变异个数
        self.bounds = 0.0                         # 适配值之和，用于选择时计算概率,公式：Fi/sum(Fi).其中Fi为个体i对应的适应值

        self.initPopulation()

    def initPopulation(self):
        """初始化种群"""
        self.lives = []
        for i in range(self.lifeCount):
            gene = [random.randint(0,1) for x in range(self.geneLenght)] # 初始化染色体
            # shuffle() 方法将序列的所有元素随机排序。
            random.shuffle(gene)
            life = Life(gene) # 生成个体
            self.lives.append(life)

    def judge(self):
        """评估，计算每一个个体的适配值"""
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life) # 获得个体的适应值
            self.bounds += life.score
            if self.best.score < life.score:
                self.best = life # 选择最优个体

    def cross(self, parent1, parent2):
        """交叉"""
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(index1, self.geneLenght - 1)
        newGene = []

        newGene.extend(parent1.gene[:index1])
        newGene.extend(parent2.gene[index1:index2])
        newGene.extend(parent1.gene[index2:])

        self.crossCount += 1
        return newGene      # 返回交叉后的parent1.gene

    def mutation(self, gene):
        """突变,两个基因互换位置"""
        index1 = random.randint(0, self.geneLenght - 1)

        newGene = gene[:]       # 产生一个新的基因序列，以免变异的时候影响父种群
        newGene[index1] = (newGene[index1]+1)%2
        if random.random() < self.mutationRate:
            self.mutation(newGene)
        self.mutationCount += 1
        return newGene

    def getOne(self):
        """选择一个个体,适应值越大，则个体被选中的概率越大"""
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """产生新后代"""
        parent1 = self.getOne()
        rate = random.random()      # 0~1的随机数

        # 按概率交叉
        if rate < self.croessRate:
            # 交叉
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene

        # 按概率突变
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)

        return Life(gene)

    def next(self):
        """产生下一代"""
        self.judge()
        newLives = []
        newLives.append(self.best)      # 把最好的个体加入下一代
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives       #更新种群
        self.generation += 1        #更新迭代次数

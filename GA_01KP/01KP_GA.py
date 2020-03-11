# 背包问题
# -*- encoding: utf-8 -*-

import random
import math
from GA import GA


class KP(object):
    def __init__(self, aLifeCount=200, ):
        # 初始化self.citys
        self.initCitys()
        self.lifeCount = aLifeCount

        self.ga = GA(aCrossRate=0.75,  # 交叉概率
                     aMutationRage=0.05,  # 突变率
                     aLifeCount=self.lifeCount,  # 种群大小
                     aGeneLenght=len(self.goods),  # 染色体长度(城市个数),其中基因为城市排列顺序。
                     aMatchFun=self.matchFun())  # 适值函数

    def initCitys(self):
        self.goods = []
        f = open("./data", "r")  # 设置文件对象
        line = f.readline()
        line = line[:-1]
        self.allGoods = float(line.split()[0])
        while line:  # 直到读取完文件
            line = f.readline()  # 读取一行文件，包括换行符
            line = line[:-1]  # 去掉换行符，也可以不去
            self.goods.append([float(line.split()[i]) for i in range(len(line.split()))])
        self.goods = self.goods[:-1]  # 去掉换行
        # print(self.goods,len(self.goods))
        f.close()  # 关闭文件

    def price(self, order):
        # order中存放着选择
        price = [0.0, 0.0]
        for i in range(0, len(self.goods)):
            price[0] += self.goods[i][0] * order[i]  # 重量
            price[1] += self.goods[i][1] * order[i]  # 价值

        return price

    def matchFun(self):
        """适值函数"""
        Max = max(self.allGoods, abs(sum(self.goods[i][0] for i in range(len(self.goods))) - self.allGoods))

        return lambda life: self.price(life.gene)[1] / (self.price(life.gene)[0] + 1 - self.allGoods) * \
                            (1 - abs(self.price(life.gene)[0] - self.allGoods) / Max) \
            if self.price(life.gene)[0] > self.allGoods \
            else self.price(life.gene)[1] * (1 - abs(self.price(life.gene)[0] - self.allGoods) / Max)

    # n为迭代次数
    def run(self, n=0):
        price = [0, 0]
        while n > 0:
            self.ga.next()
            price = self.price(self.ga.best.gene)
            n -= 1
            print("generation:", self.ga.generation, "  weights :", price[0], "----", "price :", price[1])
        print(self.ga.best.gene)
        return price


def main():
    '''多次运算，取众数即为最终值'''
    res = []
    for i in range(1):
        tsp = KP()
        res.append(tsp.run(100))
    print(res)
    print(max(res, key=res.count))


if __name__ == '__main__':
    main()

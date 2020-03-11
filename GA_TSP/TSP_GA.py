# -*- encoding: utf-8 -*-

import random
import math
from GA import GA


class TSP(object):
    def __init__(self, aLifeCount=100,):
        # 初始化self.citys
        self.initCitys()
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate=0.7,                    # 交叉概率
                     aMutationRage=0.02,                # 突变率
                     aLifeCount=self.lifeCount,         # 种群大小
                     aGeneLenght=len(self.citys),       # 染色体长度(城市个数),其中基因为城市排列顺序。
                     aMatchFun=self.matchFun())         # 适值函数

    def initCitys(self):
        self.citys = []
        """
            for i in range(34):
                  x = random.randint(0, 1000)
                  y = random.randint(0, 1000)
                  self.citys.append((x, y))
        """

        # 中国34城市经纬度(即坐标)
        """
        self.citys.append((116.46, 39.92))
        self.citys.append((117.2, 39.13))
        self.citys.append((121.48, 31.22))
        self.citys.append((106.54, 29.59))
        self.citys.append((91.11, 29.97))
        self.citys.append((87.68, 43.77))
        self.citys.append((106.27, 38.47))
        self.citys.append((111.65, 40.82))
        self.citys.append((108.33, 22.84))
        self.citys.append((126.63, 45.75))
        self.citys.append((125.35, 43.88))
        self.citys.append((123.38, 41.8))
        self.citys.append((114.48, 38.03))
        self.citys.append((112.53, 37.87))
        self.citys.append((101.74, 36.56))
        self.citys.append((117, 36.65))
        self.citys.append((113.6, 34.76))
        self.citys.append((118.78, 32.04))
        self.citys.append((117.27, 31.86))
        self.citys.append((120.19, 30.26))
        self.citys.append((119.3, 26.08))
        self.citys.append((115.89, 28.68))
        self.citys.append((113, 28.21))
        self.citys.append((114.31, 30.52))
        self.citys.append((113.23, 23.16))
        self.citys.append((121.5, 25.05))
        self.citys.append((110.35, 20.02))
        self.citys.append((103.73, 36.03))
        self.citys.append((108.95, 34.27))
        self.citys.append((104.06, 30.67))
        self.citys.append((106.71, 26.57))
        self.citys.append((102.73, 25.04))
        self.citys.append((114.1, 22.2))
        self.citys.append((113.33, 22.13))
        """
        # TSP矩阵
        """
        MAX=10000
        h=[]
        
        for i in range(10):
            for j in range(10):
                if i!=j:
                    ran=random.randint(-1,40)
                    if ran!=-1:
                        h.append(ran)
                    else:
                        h.append(MAX)
                else:
                    h.append(MAX)
            self.citys.append(h)
            h=[]
        """
        self.citys=[[10000, 34, 0, 6, 7, 13, 16, 4, 31, 37], [31, 10000, 39, 13, 29, 31, 7, 20, 25, 10], [8, 27, 10000, 1, 11, 8, 35, 19, 16, 5], [17, 3, 4, 10000, 34, 19, 11, 8, 17, 0], [35, 26, 21, 26, 10000, 25, 24, 20, 21, 1], [25, 40, 0, 17, 20, 10000, 20, 32, 21, 40], [37, 22, 31, 5, 33, 2, 10000, 1, 6, 27], [8, 13, 5, 16, 17, 29, 40, 10000, 38, 1], [39, 26, 24, 8, 31, 2, 36, 25, 10000, 12], [31, 17, 29, 37, 36, 23, 10, 12, 14, 10000]]
    def distance(self, order):
        # order中存放着城市的顺序,distance则是计算在此顺序下的总距离
        distance = 0.0
        """
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0])
                                  ** 2 + (city1[1] - city2[1]) ** 2)
        
        """
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            distance+=self.citys[index1][index2]
        return distance

    # 适值函数  对distance取倒数,使得其满足适值越大则选中概率越大
    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    # n为迭代次数
    def run(self, n=0):
        distance=0
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
        #   print(("%d : %f") % (self.ga.generation, distance))
            n -= 1
        # for i in range(10):
        #     print(i+1,"----",self.citys[i])
        # print("---------------")
        # c=[self.ga.best.gene[i]+1 for i in  range(10)]
        # print(c)
        return distance



def main():
    '''多次运算，取众数即为最终值'''
    res=[]
    for i in range(100):
        tsp = TSP()
        res.append(tsp.run(100))
    print(res)
    print(max(res, key=res.count))


if __name__ == '__main__':
    main()

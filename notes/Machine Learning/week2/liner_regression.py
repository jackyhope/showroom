# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 11:49 
# @Author : Zhy

'''
假设你是一家餐馆的首席执行官，正在考虑不同的城市开设一个新的分店。该连锁店已经在各个城市拥有卡车，而且你有来自城市的利润和人口数据。
您希望使用这些数据来帮助您选择将哪个城市扩展到下一个城市。
'''

import numpy as np
import pandas as pd
import matplotlib.pylab as plt

def computCost(X,y,theta):
    inner=np.power((X@theta.T)-y,2)
    return np.sum(inner)/(2*len(X))

def gradientDescent(X,y,theta,alpha,epoch):
    cost = []
    for i in range(epoch):
        # print((alpha/len(X)*(X@theta.T-y).T).shape)
        # print(X.shape)
        theta=theta-alpha/len(X)*(X@theta.T-y).T@X
        cost.append(computCost(X,y,theta))
    return theta,cost

if __name__ == '__main__':

    '''散点图'''
    data=pd.read_csv('ex1data1.txt',header=None,names=['Population','Profit'])
    plt.scatter(data['Population'],data['Profit'],marker='x',c='r')
    # plt.show()
    data.insert(0,'Ones',1)
    X=np.matrix(data.iloc[:,:-1])
    y=np.matrix(data.iloc[:,-1:])
    print(X.shape,y.shape)
    theta=np.matrix(np.zeros((1,2)))

    '''梯度下降法'''
    alpha,epoch=0.01,1500
    theta,cost=gradientDescent(X,y,theta,alpha,epoch)
    print(theta)

    '''调试'''
    x = np.linspace(4,24,100)
    f = theta[0, 0] + (theta[0, 1] * x)
    plt.plot(x,f,c='b')
    plt.show()
    x1=np.linspace(1,1500,1500)
    y=np.array(cost)
    plt.plot(x1,y,c='g')
    plt.show()



















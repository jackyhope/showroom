# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 15:14 
# @Author : Zhy

'''
假设你正在出售房屋，希望制定一个合适的价格，你收集到一个数据集，其中有2个变量（房子的大小，卧室的数量）和目标（房子的价格），据此制定价格。
'''

import pandas as pd
import numpy as np
from liner_regression import gradientDescent
import matplotlib.pylab as plt

def NormalEquations(X,y):
    theta=np.linalg.inv(X.T@X)@X.T@y
    return theta


if __name__ == '__main__':

    '''数据处理'''
    data=pd.read_csv('ex1data2.txt',header=None,names=['Sizes','Bedrooms','Price'])
    data=(data-data.mean())/data.std()
    print(data.describe())
    data.insert(0,'Ones',1)
    X=np.matrix(data.iloc[:,:-1])
    y=np.matrix(data.iloc[:,-1:])
    print(X.shape,y.shape)
    theta=np.zeros((1,3))


    '''梯度下降法，可视化'''
    x=np.linspace(1,1500,1500)
    alpha, epoch = 0.01, 1500
    theta, cost = gradientDescent(X, y, theta, alpha, epoch)
    plt.plot(x,cost,c='r')
    plt.show()


    '''正规方程法'''
    theta=NormalEquations(X, y)
    print(theta)





# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 15:57 
# @Author : Zhy

'''
假设你是一所大学的行政管理人员，你想根据两门考试的结果，来决定每个申请人是否被录取。你有以前申请人的历史数据，
可以将其用作逻辑回归训练集.
'''

import numpy as np
import pandas as pd
import matplotlib.pylab as plt

def  sigmoid(z):
    return 1/(1+np.exp(-z))
def cost(X,y,theta):
    first=(-y)*np.log(sigmoid(X@theta.T))
    second=(1-y)*np.log(1-sigmoid(X@theta.T))
    inner=np.sum(first-second)
    return 1/len(X)*inner
def gradientDescent(X,y,theta,alpha,epoch):
    cost_1 = []
    for i in range(epoch):
        theta=theta-alpha/len(X)*(sigmoid(X@theta.T)-y).T@X
        # print(cost(X,y,theta))
        cost_1.append(cost(X,y,theta))
    return theta,cost_1



if __name__ == '__main__':

    '''散点图'''
    data=pd.read_csv('ex2data1.txt',header=None,names=['exam1','exam2','admitted'])
    data.insert(0,'Ones',1)
    print(data.describe())
    positive=data[data['admitted'].isin(['1'])]
    negetive=data[data['admitted'].isin(['0'])]
    plt.scatter(positive['exam1'],positive['exam2'],marker='x',c='black',label='admitted')
    plt.scatter(negetive['exam1'],negetive['exam2'],marker='o',c='red',label='not admintted')
    plt.legend(loc='upper right')    #图例位置
    # plt.show()

    '''损失函数、梯度下降法'''
    X,y=np.array(data.iloc[:,:-1]),np.array(data.iloc[:,-1:])
    theta = np.zeros((1, 3))
    print(X.shape,y.shape,theta.shape)
    alpha,epoch=0.001,500000
    theta, cost_1=gradientDescent(X, y, theta, alpha, epoch)
    print(theta)

    # x1=np.linspace(0,5000,500000)
    # plt.plot(x1,cost_1)
    # plt.show()

    x1=np.linspace(0,100,100)
    print(theta[0][0])
    x2=(-theta[0][0]-theta[0][1]*x1)/theta[0][2]
    plt.plot(x1,x2,c='y')
    plt.show()







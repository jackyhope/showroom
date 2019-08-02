# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 19:56 
# @Author : Zhy

'''
假设你是工厂的生产主管，你有一些芯片在两次测试中的测试结果。对于这两次测试，你想决定是否芯片要被接受或抛弃。
为了帮助你做出艰难的决定，你拥有过去芯片的测试数据集，从其中你可以构建一个逻辑回归模型。
'''

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from Logistic_Regression import gradientDescent,cost,sigmoid

'''多项式的特征映射'''
def feature_mapping(x1,x2,power):
    dict_data={}
    for i in  range(power+1):
        for p in range(i+1):
            dict_data['f{}{}'.format(i,p)]=np.power(x1,i-p)*np.power(x2,p)
    return pd.DataFrame(dict_data)
'''正则化'''
def cost_reg(X,y,theta,l):
    theta_1=theta[0][1:]
    reg=(l/(2*len(X)))*np.sum(np.power(theta_1,2))
    cost_1=cost(X,y,theta)+reg
    return cost_1
def gradient_Descent(X,y,theta,alpha,epoch,l):
    cost_1 = []
    for i in range(epoch):
        theta=theta-alpha*(1/len(X)*(sigmoid(X@theta.T)-y).T@X+l/len(X)*theta)
        # print(cost_reg(X,y,theta,l))
        cost_1.append(cost_reg(X,y,theta,l))
    return theta,cost_1

if __name__ == '__main__':

    data=pd.read_csv('ex2data2.txt',header=None,names=['test1','test2','admitted'])
    positive=data[data['admitted'].isin(['1'])]
    negetive=data[data['admitted'].isin(['0'])]
    plt.scatter(positive['test1'],positive['test2'],c='b',marker='o')
    plt.scatter(negetive['test1'],negetive['test2'],c='r',marker='x')
    # plt.show()
    data_1=feature_mapping(data['test1'],data['test2'],6)
    X,y=np.array(data_1),np.array(data.iloc[:,-1:])
    theta=np.array(np.zeros((1,X.shape[1])))

    #正则化
    alpha_1, epoch_1, l_1=0.7,5000,2
    theta_reg, cost_2=gradient_Descent(X, y, theta,alpha_1,epoch_1,l_1)
    print(theta_reg)
    plt.scatter(positive['test1'], positive['test2'], c='b', marker='o')
    plt.scatter(negetive['test1'], negetive['test2'], c='r', marker='x')
    x1 = np.linspace(-1, 1.5, 250)
    xx1, yy1 = np.meshgrid(x1, x1)                                #生成网格点坐标矩阵
    z1 = np.array(feature_mapping(xx1.ravel(), yy1.ravel(), 6))   #racel():将多维数组降位一维
    z1 = z1 @ theta_reg.T
    z1 = z1.reshape(xx1.shape)
    plt.contour(xx1, yy1, z1, 0)   #绘制等高线，0代表只生成一条等高线
    plt.show()
    x3 = np.linspace(1, 5000, 5000)
    plt.plot(x3, cost_2, c='r')
    plt.show()







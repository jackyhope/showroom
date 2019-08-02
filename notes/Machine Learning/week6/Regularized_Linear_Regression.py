# -*- coding: utf-8 -*- 
# @Time : 2019/1/24 15:03 
# @Author : Zhy

'''
通过水库中的水位变化，从而预测大坝流出的水量，使用正则化的线性回归模型
'''

import pandas as pd
import numpy as np
from scipy.io import loadmat
import matplotlib.pylab as plt
import scipy.optimize as opt

def costReg(theta, X, y, l):
    cost = ((X @ theta - y.flatten()) ** 2).sum()
    regterm = l * (theta[1:] @ theta[1:])
    return (cost + regterm) / (2 * len(X))
def trainLinearReg(X, y, l):
    def gradientReg(theta, X, y, l):
        """梯度"""
        grad = (X @ theta - y.flatten()) @ X
        regterm = l * theta
        regterm[0] = 0  # 不惩罚theta0
        return (grad + regterm) / len(X)
    theta = np.zeros(X.shape[1])
    res = opt.minimize(fun=costReg,
                       x0=theta,
                       args=(X, y ,l),
                       method='TNC',
                       jac=gradientReg)
    return res.x


if __name__ == '__main__':
    data=loadmat('ex5data1.mat')
    print(data.keys())
    X,y,Xval,yval,Xtest,ytest=data['X'],data['y'],data['Xval'],data['yval'],data['Xtest'],data['ytest']
    plt.scatter(X,y,c='r',marker='x')
    # plt.show()
    X=np.insert(X, 0, 1, axis=1)
    Xval=np.insert(Xval, 0, 1, axis=1)
    Xtest=np.insert(Xtest, 0, 1, axis=1)
    print(X.shape,Xval.shape,Xtest.shape)

    fit_theta = trainLinearReg(X, y, 0)
    plt.plot(X[:, 1], X @ fit_theta)
    plt.show()




# -*- coding: utf-8 -*-
# @Time : 2019/1/24 16:01 
# @Author : Zhy 

'''
研究具有不同偏差-方差属性的模型,高偏差意味着欠拟合，高方差意味着过拟合
'''

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat
from Regularized_Linear_Regression import trainLinearReg,costReg

def plot_learning_curve(X, y, Xval, yval, l):
    '''学习曲线'''
    xx = range(1, len(X) + 1)
    training_cost, cv_cost = [], []
    for i in xx:
        res = trainLinearReg(X[:i], y[:i], l)
        training_cost_i = costReg(res, X[:i], y[:i], 0)
        cv_cost_i = costReg(res, Xval, yval, 0)
        training_cost.append(training_cost_i)
        cv_cost.append(cv_cost_i)

    x1=np.linspace(1,len(X),len(X))
    plt.plot(x1,training_cost,c='r',label='training cost')
    plt.plot(x1,cv_cost,c='blue',label='cv cost')
    plt.legend()
    plt.xlabel('Number of training examples')
    plt.ylabel('Error')
    plt.title('Learning curve for linear regression')
    plt.grid(True)
    plt.show()
def genPolyFeatures(X, power):
    """添加多项式特征，每次在array的最后一列插入第二列的i次方（第一列为偏置）"""
    Xpoly = X.copy()
    for i in range(2, power + 1):
        Xpoly = np.insert(Xpoly, Xpoly.shape[1], np.power(Xpoly[:,1], i), axis=1)
    return Xpoly
def get_means_std(X):
    """获取训练集的均值和误差，用来标准化所有数据。"""
    means = np.mean(X,axis=0)
    stds = np.std(X,axis=0,ddof=1)  # ddof=1 means 样本标准差
    return means, stds
def featureNormalize(X,means, stds):
    """标准化"""
    X_norm = X.copy()
    X_norm[:,1:] = X_norm[:,1:] - means[1:]
    X_norm[:,1:] = X_norm[:,1:] / stds[1:]
    return X_norm
def plot_fit(means, stds, l):
    """画出拟合曲线"""
    theta = trainLinearReg(X_norm, y, l)
    x = np.linspace(-75, 55, 50)
    xmat = x.reshape(-1, 1)
    xmat = np.insert(xmat, 0, 1, axis=1)
    Xmat = genPolyFeatures(xmat, 6)
    Xmat_norm = featureNormalize(Xmat, means, stds)
    plt.scatter(data['X'], data['y'], c='r', marker='x')

    plt.plot(x, Xmat_norm @ theta, 'b--')
    plt.show()


if __name__ == '__main__':

    #线性回归
    data=loadmat('ex5data1.mat')
    X,y,Xval,yval,Xtest,ytest=data['X'],data['y'],data['Xval'],data['yval'],data['Xtest'],data['ytest']

    X = np.insert(X, 0, 1, axis=1)
    Xval = np.insert(Xval, 0, 1, axis=1)
    Xtest = np.insert(Xtest, 0, 1, axis=1)
    # plot_learning_curve(X, y, Xval, yval, 0)

    #多项式回归
    means, stds=get_means_std(genPolyFeatures(X, 6))
    X_norm = featureNormalize(genPolyFeatures(X, 6),means, stds)
    Xval_norm=featureNormalize(genPolyFeatures(Xval, 6),means, stds)
    Xtest_norm=featureNormalize(genPolyFeatures(Xtest, 6),means, stds)
    l=1
    plot_fit(means, stds, l)
    plot_learning_curve(X_norm, y, Xval_norm, yval, l)

    #寻找最佳l
    lambdas = [0., 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1., 3., 10.]
    errors_train, errors_val = [], []
    for l in lambdas:
        theta = trainLinearReg(X_norm, y, l)
        errors_train.append(costReg(theta, X_norm, y, 0))  # 记得把lambda = 0
        errors_val.append(costReg(theta, Xval_norm, yval, 0))

    plt.figure(figsize=(8, 5))
    plt.plot(lambdas, errors_train, label='Train')
    plt.plot(lambdas, errors_val, label='Cross Validation')
    plt.legend()
    plt.xlabel('lambda')
    plt.ylabel('Error')
    plt.grid(True)
    plt.show()






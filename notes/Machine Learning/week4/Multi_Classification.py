# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 13:56 
# @Author : Zhy

'''
使用逻辑回归和神经网络,识别手写数字(从0到9)。
'''

import pandas as pd
import numpy as np
from scipy.io import loadmat
import matplotlib.pylab as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))
'''可视化'''
def plot_image(X):
    fig,ax_array=plt.subplots(nrows=10,ncols=10,figsize=(8,8),sharey=True, sharex=True)
    sample_idx = np.random.choice(np.arange(X.shape[0]), 100)
    sample_images = X[sample_idx, :]
    for i in range(10):
        for j in range(10):
            ax_array[i,j].matshow(sample_images[10*i+j].reshape(20,20))

    plt.xticks([])  #去掉坐标轴
    plt.yticks([])
    plt.show()
def reg_cost(X,y,theta,l):
    theta_1=theta[1:]
    first=(-y)*np.log(sigmoid(X@theta.T))
    second=(1-y)*np.log(sigmoid(1-X@theta.T))
    inner = np.sum(first - second)
    reg=(l/(2*len(X)))*np.sum(np.power(theta_1,2))
    return 1/len(X)*inner+reg
def gradient_Descent(X,y,theta,alpha,epoch,l):
    cost_1 = []
    for i in range(epoch):
        theta=theta-alpha*(1/len(X)*(sigmoid(X@theta.T)-y).T@X+l/len(X)*theta)
        cost_2=reg_cost(X,y,theta,l)
        print(cost_2)
        cost_1.append(cost_2)
    return theta,cost_1

def one_vs_all(X, y, l, K):

    all_theta = np.zeros((K, X.shape[1]))
    for i in range(1, K + 1):
        theta = np.zeros((1,X.shape[1]))
        alpha,epoch=0.28,1000
        y_i = np.array([1 if label == i else 0 for label in y])
        theta_1,cost_1=gradient_Descent(X, y_i, theta, alpha, epoch, l)
        print(theta_1,cost_1)

        x1=np.linspace(1,100,100)
        plt.plot(x1,cost_1,c='r')
        plt.show()
        all_theta[i - 1, :] = theta_1
    return all_theta


if __name__ == '__main__':
    data=loadmat('ex3data1.mat')
    X,y=np.array(data['X']),np.array(data['y'])
    theta=np.array((1,X.shape[1]))
    print(X.shape,y.shape)
    # plot_image(X)
    l, K=1,10
    all_theta=one_vs_all(X, y, l, K)







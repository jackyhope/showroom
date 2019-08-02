# -*- coding: utf-8 -*- 
# @Time : 2019/1/23 11:35 
# @Author : Zhy

'''实现反向传播算法来学习神经网络的参数'''

import pandas as pd
import numpy as np
from scipy.io import loadmat
import matplotlib.pylab as plt
import scipy.optimize as opt
from sklearn.metrics import classification_report

def plot_100_images(X):
    """随机画100个数字"""
    index = np.random.choice(range(5000), 100)
    images = X[index]
    fig, ax_array = plt.subplots(10, 10, sharey=True, sharex=True, figsize=(8, 8))
    for r in range(10):
        for c in range(10):
            ax_array[r, c].matshow(images[r*10 + c].reshape(20,20), cmap='gray_r')
    plt.xticks([])
    plt.yticks([])
    plt.show()
def expand_y(y):
    '''把y中每个类别转化为一个向量，对应的lable值在向量对应位置上置为1'''
    result=[]
    for i in y :
        y_array=np.zeros(10)
        y_array[i-1]=1
        result.append(y_array)
    return np.array(result)
def serialize(a, b):
    '''展开参数'''
    return np.r_[a.flatten(), b.flatten()]
def deserialize(seq):
    '''提取参数'''
    return seq[:25*401].reshape(25, 401), seq[25*401:].reshape(10, 26)
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
def feed_forward(theta, X, ):
    '''得到每层的输入和输出'''
    t1, t2 = deserialize(theta)
    # 前面已经插入过偏置单元，这里就不用插入了
    a1 = X
    z2 = a1 @ t1.T
    a2 = np.insert(sigmoid(z2), 0, 1, axis=1)
    z3 = a2 @ t2.T
    a3 = sigmoid(z3)
    return a1, z2, a2, z3, a3
def regularized_cost(theta, X, y, l=1):
    '''正则化时忽略每层的偏置项，也就是参数矩阵的第一列'''
    def cost(theta, X, y):
        a1, z2, a2, z3, h = feed_forward(theta, X)
        J = 0
        for i in range(len(X)):
            first = - y[i] * np.log(h[i])
            second = (1 - y[i]) * np.log(1 - h[i])
            J = J + np.sum(first - second)
        J = J / len(X)
        return J
    t1, t2 = deserialize(theta)
    reg = np.sum(t1[:,1:] ** 2) + np.sum(np.power(t2[:,1:],2))
    return l/(2*len(X))*reg + cost(theta,X,y)
def gradient(theta, X, y):
    '''
    return 所有参数theta的梯度，故梯度D(i)和参数theta(i)同shape。
    '''
    def sigmoid_gradient(z):
        '''S函数求导'''
        return sigmoid(z) * (1 - sigmoid(z))
    t1, t2 = deserialize(theta)
    a1, z2, a2, z3, h = feed_forward(theta, X)
    d3 = h - y  # (5000, 10)
    d2 = d3 @ t2[:, 1:] * sigmoid_gradient(z2)  # (5000, 25)  误差
    D2 = d3.T @ a2  # (10, 26)   偏导
    D1 = d2.T @ a1  # (25, 401)
    D = (1 / len(X)) * serialize(D1, D2)  # (10285,)
    return D
def a_numeric_grad(plus, minus,e):
    """对每个参数theta_i计算数值梯度，即理论梯度。"""
    return (regularized_cost(plus, X, y) - regularized_cost(minus, X, y)) / (e * 2)
def regularized_gradient(theta, X, y, l=1):
    """正则化，不惩罚偏置单元的参数"""
    D1, D2 = deserialize(gradient(theta, X, y))
    t1[:, 0] = 0
    t2[:, 0] = 0
    reg_D1 = D1 + (l / len(X)) * t1
    reg_D2 = D2 + (l / len(X)) * t2
    return serialize(reg_D1, reg_D2)
def gradient_checking(theta, X, y, e):
    numeric_grad = []
    for i in range(len(theta)):
        plus = theta.copy()  # deep copy otherwise you will change the raw theta
        minus = theta.copy()
        plus[i] = plus[i] + e
        minus[i] = minus[i] - e
        grad_i = a_numeric_grad(plus, minus,e)
        numeric_grad.append(grad_i)

    numeric_grad = np.array(numeric_grad)
    analytic_grad = regularized_gradient(theta, X, y)
    diff = np.linalg.norm(numeric_grad - analytic_grad) / np.linalg.norm(numeric_grad + analytic_grad)
    print('梯度检测差异值：',diff)
def nn_training(X, y):
    #训练，优化参数
    init_theta = np.random.uniform(-0.12, 0.12, 10285) # 25*401 + 10*26
    res = opt.minimize(fun=regularized_cost,
                       x0=init_theta,
                       args=(X, y, 1),
                       method='TNC',
                       jac=regularized_gradient,
                       options={'maxiter': 400})
    return res
def accuracy(res, X, y):
    h = feed_forward(res.x, X)[4]
    y_pred = np.argmax(h, axis=1) + 1
    print(classification_report(y, y_pred))



if __name__ == '__main__':

    data=loadmat('ex4data1.mat')
    raw_X, raw_y=data['X'],data['y'].flatten()
    # plot_100_images(raw_X)   #随机显示样本图片
    X = np.insert(raw_X, 0, 1, axis=1)
    y=expand_y(raw_y)
    print(X.shape,y.shape)
    data_weight = loadmat('ex4weights.mat')
    t1,t2=data_weight['Theta1'],data_weight['Theta2']
    print(t1.shape,t2.shape)
    theta = serialize(t1, t2)
    print(theta.shape)   #扁平化参数，25*401+10*26=10285
    # gradient_checking(theta, X, y, 0.0001)   #梯度检验
    res = nn_training(X, y)  # 训练
    accuracy(res, X, raw_y)




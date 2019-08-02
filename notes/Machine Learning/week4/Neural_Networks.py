# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 16:23 
# @Author : Zhy 

'''
logistic回归不能形成更复杂的假设，因为它只是一个线性分类器。接下来我们用神经网络来尝试下，
神经网络可以实现非常复杂的非线性的模型。我们将利用已经训练好了的权重进行预测。
'''

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat
from Multi_Classification import sigmoid


if __name__ == '__main__':

    data= loadmat('ex3weights.mat')
    theta1,theta2=data['Theta1'],data['Theta2']
    print(theta1.shape,theta2.shape)

    data_1=loadmat('ex3data1.mat')
    y=data_1['y']
    y = y.flatten()
    X=np.array(data_1['X'])
    X = np.insert(X, 0, values=np.ones(X.shape[0]), axis=1)
    print(X.shape,y.shape)

    a1 = X
    z2 = a1 @ theta1.T
    z2 = np.insert(z2, 0, 1, axis=1)
    a2=sigmoid(z2)
    z3= a2 @ theta2.T
    a3=sigmoid(z3)

    y_pred = np.argmax(a3, axis=1) + 1     #np.argmax()返回最大值的索引

    accuracy = np.mean(y_pred == y)
    print('accuracy = {0}%'.format(accuracy * 100))




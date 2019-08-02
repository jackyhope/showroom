# -*- coding: utf-8 -*- 
# @Time : 2019/1/24 18:32 
# @Author : Zhy

'''支持向量机'''

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat
from sklearn import svm

def plot_data(X,y):
    plt.scatter(X[:,0],X[:,1],c=y.flatten(),cmap='rainbow')   #cmap: 颜色图谱
    plt.show()



if __name__ == '__main__':
    data=loadmat('ex6data1.mat')
    X,y=data['X'],data['y']
    print(X.shape,y.shape)
    plot_data(X, y)



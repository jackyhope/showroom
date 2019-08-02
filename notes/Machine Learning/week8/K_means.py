# -*- coding: utf-8 -*- 
# @Time : 2019/1/24 19:10 
# @Author : Zhy

'''实现K-means算法并将其用于图像压缩。通过减少图像中出现的颜色的数量，只剩下那些在图像中最常见的颜色'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from skimage import io


def initCentroids(X, K):
    """随机初始化"""
    m, n = X.shape
    idx = np.random.choice(m, K)
    centroids = X[idx]
    return centroids
def findClosestCentroids(X, centroids):
    idx = []
    for i in range(len(X)):
        minus = X[i] - centroids
        dist = minus[:, 0] ** 2 + minus[:, 1] ** 2    #样本与各的簇中心距离
        ci = np.argmin(dist)                          #返回最小值的索引
        idx.append(ci)
    return np.array(idx)
def computeCentroids(X, idx):
    '''重新计算每个簇中心'''
    centroids = []
    for i in range(len(np.unique(idx))):  # np.unique():去重，并按元素由小到大返回数组
        u_k = X[idx==i].mean(axis=0)      # 求每列的平均值
        centroids.append(u_k)
    return np.array(centroids)
def plotData(X, centroids, idx):
    """
    可视化数据，并自动分开着色。
    idx: 最后一次迭代生成的idx向量，存储每个样本分配的簇中心点的值
    centroids: 包含每次中心点历史记录
    """
    colors = ['b', 'g', 'gold', 'darkorange', 'salmon', 'olivedrab','maroon', 'navy', 'sienna', 'tomato', 'lightgray', 'gainsboro''coral', 'aliceblue', 'dimgray', 'mintcream','mintcream']
    assert len(centroids[0]) <= len(colors), 'colors not enough '   #当assert的条件不成立后，抛出条件后的错误提示信息

    subX = []  # 分号类的样本点
    for i in range(centroids[0].shape[0]):
        x_i = X[idx == i]
        subX.append(x_i)

    # 分别画出每个簇的点，并着不同的颜色
    plt.figure(figsize=(8, 5))
    for i in range(len(subX)):
        xx = subX[i]
        plt.scatter(xx[:, 0], xx[:, 1], c=colors[i], label='Cluster %d' % i)
    plt.legend()
    plt.grid(True)
    plt.xlabel('x1', fontsize=14)
    plt.ylabel('x2', fontsize=14)
    plt.title('Plot of X Points', fontsize=16)

    # 画出簇中心点的移动轨迹
    xx, yy = [], []
    for centroid in centroids:
        xx.append(centroid[:, 0])
        yy.append(centroid[:, 1])
    plt.plot(xx, yy, 'rx--', markersize=8)
    plt.show()
def runKmeans(X, centroids):

    centroids_all = []
    centroids_all.append(centroids)
    flag=True
    while flag:
        idx = findClosestCentroids(X, centroids)
        centroid_i = computeCentroids(X, idx)
        if str(centroid_i)==str(centroids):
            flag=False
        else:
            centroids_all.append(centroid_i)
            centroids=centroid_i

    return idx, centroids_all


if __name__ == '__main__':
    data=loadmat('ex7data2.mat')
    X=data['X']
    print(X.shape)

    # init_centroids = initCentroids(X, 3)   #随机初始簇中心
    # idx, centroids_all = runKmeans(X, init_centroids)
    # plotData(X, centroids_all, idx)

    A=io.imread('bird_small.png')
    # plt.imshow(A)
    # plt.show()
    A=A/255
    X = A.reshape(-1, 3)
    K=10
    centroids = initCentroids(X, K)
    idx, centroids_all = runKmeans(X, centroids)
    plotData(X, centroids_all, idx)

    img = np.zeros(X.shape)
    centroids = centroids_all[-1]
    for i in range(len(centroids)):
        img[idx == i] = centroids[i]
    img = img.reshape((128, 128, 3))
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(A)
    axes[1].imshow(img)
    plt.show()





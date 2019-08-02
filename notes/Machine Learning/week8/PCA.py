# -*- coding: utf-8 -*- 
# @Time : 2019/1/25 8:54 
# @Author : Zhy

'''
运用PCA来实现降维: 1.标准化数据；2.计算数据的方差矩阵； 3.用SVD计算特征向量
'''

from K_means import *

def featureNormalize(X):
    means=X.mean(axis=0)
    stds=X.std(axis=0,ddof=1)
    X_norm=(X-means)/stds
    return X_norm,means,stds
def pca(X):
    sigma = (X.T @ X) / len(X)
    U, S, V = np.linalg.svd(sigma)
    return U, S, V

def plot_1():
    plt.scatter(X[:, 0], X[:, 1], marker='x', c='b')
    print(U[:, 0])
    plt.plot([means[0], means[0] + 1.5 * S[0] * U[0, 0]],
             [means[1], means[1] + 1.5 * S[0] * U[0, 1]],
             c='r', linewidth=3, label='First Principal Component')
    plt.plot([means[0], means[0] + 1.5 * S[1] * U[1, 0]],
             [means[1], means[1] + 1.5 * S[1] * U[1, 1]],
             c='g', linewidth=3, label='Second Principal Component')
    plt.grid()
    plt.axis("equal")
    plt.legend()
    plt.show()
def displayData(X, row, col):
    fig, axs = plt.subplots(row, col, figsize=(8, 8))
    for r in range(row):
        for c in range(col):
            axs[r][c].imshow(X[r * col + c].reshape(32, 32).T, cmap='Greys_r')
            axs[r][c].set_xticks([])
            axs[r][c].set_yticks([])
    plt.show()

if __name__ == '__main__':
    mat = loadmat('ex7data1.mat')
    X = mat['X']
    print(X.shape)
    X_norm,means,stds = featureNormalize(X)
    U, S, V = pca(X_norm)
    # plot_1()
    mat_1 = loadmat('ex7faces.mat')
    X_1 = mat_1['X']
    print(X_1.shape)
    # displayData(X_1, 10, 10)    #原图
    X_norm_1, means_1, stds_1 = featureNormalize(X_1)
    U_1, S_1, V_1 = pca(X_norm_1)
    displayData(U_1[:, :36].T, 6, 6)  #降维后的图片




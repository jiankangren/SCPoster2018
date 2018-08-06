#!/usr/bin/python
# coding: utf-8

'''
Created on Jun 1, 2011
Update  on 2017-05-18
Author: Peter Harrington/片刻
GitHub：https://github.com/apachecn/MachineLearning
'''
from numpy import *
import matplotlib.pyplot as plt
import sys
import array
import os

if len(sys.argv) < 1 :
    print 'usage: python %s <file.dat' % sys.argv[0]
    sys.exit(0)

print sys.argv[1]




#print(__doc__)


def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split() for line in fr.readlines()]
    print shape(stringArr)
   # print stringArr
    datArr = [map(float, line) for line in stringArr]
    return mat(datArr)
def storeMatrix(filename,m1):
    mat1 = matrix(m1)
    with open(filename,'wb') as f:
    	for line in mat1:
        	savetxt(f, line.real, fmt='%f')
        


def pca(dataMat, topNfeat=9999999):
    """pca

    Args:
        dataMat   原数据集矩阵
        topNfeat  应用的N个特征
    Returns:
        lowDDataMat  降维后数据集
        reconMat     新的数据集空间
    """
    storeMatrix('dataMat.txt',dataMat)
    # 计算每一列的均值
    meanVals = mean(dataMat, axis=0)
    # print 'meanVals', meanVals
    storeMatrix('mean.txt',meanVals)
    # 每个向量同时都减去 均值
    meanRemoved = dataMat - meanVals
    # print 'meanRemoved=', meanRemoved
    storeMatrix('meanRemoved.txt',meanRemoved)
    # cov协方差=[(x1-x均值)*(y1-y均值)+(x2-x均值)*(y2-y均值)+...+(xn-x均值)*(yn-y均值)+]/(n-1)
    '''
    方差：（一维）度量两个随机变量关系的统计量
    协方差： （二维）度量各个维度偏离其均值的程度
    协方差矩阵：（多维）度量各个维度偏离其均值的程度

    当 cov(X, Y)>0时，表明X与Y正相关；(X越大，Y也越大；X越小Y，也越小。这种情况，我们称为“正相关”。)
    当 cov(X, Y)<0时，表明X与Y负相关；
    当 cov(X, Y)=0时，表明X与Y不相关。
    '''
    covMat = cov(meanRemoved, rowvar=0)
    #storeMatrix('covMat',covMat)
    # eigVals为特征值， eigVects为特征向量
    eigVals, eigVects = linalg.eig(mat(covMat))
   # eigVals, eigVects = linalg.eig(mat(covMat))
    storeMatrix('eigVals_notsorted.txt',eigVals)
    storeMatrix('eigVects.txt',eigVects)

    # print 'eigVals=', eigVals
    # print 'eigVects=', eigVects
    # 对特征值，进行从小到大的排序，返回从小到大的index序号
    # 特征值的逆序就可以得到topNfeat个最大的特征向量
    '''
    >>> x = np.array([3, 1, 2])
    >>> np.argsort(x)
    array([1, 2, 0])  # index,1 = 1; index,2 = 2; index,0 = 3
    >>> y = np.argsort(x)
    >>> y[::-1]
    array([0, 2, 1])
    >>> y[:-3:-1]
    array([0, 2])  # 取出 -1, -2
    >>> y[:-6:-1]
    array([0, 2, 1])
    '''
    eigValInd = argsort(eigVals)
    storeMatrix('eigVals_sorted.txt',eigValInd)
    # print 'eigValInd1=', eigValInd

    # -1表示倒序，返回topN的特征值[-1 到 -(topNfeat+1) 但是不包括-(topNfeat+1)本身的倒叙]
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    # print 'eigValInd2=', eigValInd
    # 重组 eigVects 最大到最小
    redEigVects = eigVects[:, eigValInd]
    storeMatrix('redEigVects.txt',redEigVects)
    # print 'redEigVects=', redEigVects.T
    # 将数据转换到新空间
    # print "---", shape(meanRemoved), shape(redEigVects)
    lowDDataMat = meanRemoved * redEigVects
    storeMatrix('lowDDataMat.txt',lowDDataMat)
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    storeMatrix('reconMat.txt',reconMat)
    # print 'lowDDataMat=', lowDDataMat
    # print 'reconMat=', reconMat
    print shape(lowDDataMat)[1]*shape(lowDDataMat)[0]
    print shape(reconMat)[1]*shape(reconMat)[0]
    print shape(meanVals)[0]*shape(meanVals)[1]
    return lowDDataMat, reconMat


def replaceNanWithMean(filename):
    #datMat = loadDataSet('/home/luo//Luo/PCA/MachineLearning/input/13.PCA/secom.data', ' ')
    datMat = loadDataSet(filename, ' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        # 对value不为NaN的求均值
        # .A 返回矩阵基于的数组
        meanVal = mean(datMat[nonzero(~isnan(datMat[:, i].A))[0], i])
        # 将value为NaN的值赋值为均值
        datMat[nonzero(isnan(datMat[:, i].A))[0],i] = meanVal
    return datMat


def show_picture(dataMat, reconMat):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s=90)
    ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s=50, c='red')
    plt.show()


def analyse_data(dataMat):
    meanVals = mean(dataMat, axis=0)
    meanRemoved = dataMat-meanVals
    covMat = cov(meanRemoved, rowvar=0)
    eigvals, eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigvals)

    topNfeat = 20
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    cov_all_score = float(sum(eigvals))
    sum_cov_score = 0
    for i in range(0, len(eigValInd)):
        line_cov_score = float(eigvals[eigValInd[i]])
        sum_cov_score += line_cov_score
        '''
        我们发现其中有超过20%的特征值都是0。
        这就意味着这些特征都是其他特征的副本，也就是说，它们可以通过其他特征来表示，而本身并没有提供额外的信息。

        最前面15个值的数量级大于10^5，实际上那以后的值都变得非常小。
        这就相当于告诉我们只有部分重要特征，重要特征的数目也很快就会下降。

        最后，我们可能会注意到有一些小的负值，他们主要源自数值误差应该四舍五入成0.
        '''
        print '%s, %s%%, %s%%' % (format(i+1, '2.0f'), format(line_cov_score/cov_all_score*100, '4.5f'), format(sum_cov_score/cov_all_score*100, '4.5f'))


if __name__ == "__main__":
    # # 加载数据，并转化数据类型为float
   # dataMat = loadDataSet('/home/luo//Luo/PCA/MachineLearning/input/13.PCA/testSet.txt')
    filename=sys.argv[1]
    dataMat = loadDataSet(filename)
    # # 只需要1个特征向量
    #print shape(dataMat)
    #lowDmat, reconMat = pca(dataMat, 1)
    # # 只需要2个特征向量，和原始数据一致，没任何变化
    #lowDmat, reconMat = pca(dataMat, 2)
    #print shape(lowDmat)
    #print lowDmat
    #print shape(reconMat)
    #delta=reconMat-dataMat
    #for row in delta :
    #	print row
    #show_picture(dataMat, reconMat)

    # 利用PCA对半导体制造数据降维
    # dataMat = replaceNanWithMean(filename)
    #print shape(dataMat)
    #print dataMat
    # 分析数据
   # analyse_data(dataMat)
    lowDmat, reconMat = pca(dataMat, 1)
    #show_picture(dataMat, reconMat)
   # analyse_data(dataMat)
    delta=dataMat-reconMat 
    storeMatrix('delta.txt',delta)
    #for row in delta :
    #	print row


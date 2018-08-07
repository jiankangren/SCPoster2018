

import numpy as np

import matplotlib.pyplot as plt
import sys
import array
import os


def rebuild2(u,sigma,v,k):
    uk = u[:,:k] 
    sigma_k=np.diag(sigma[:k])
    vk = v[:k,:] 
    dot1 = np.dot(uk, sigma_k)
    return np.dot(dot1,vk)  
def storeMatrix(filename,m1):
    mat1 = np.matrix(m1)
    with open(filename,'wb') as f:
    	for line in mat1:
        	np.savetxt(f, line.real, fmt='%f')

def analyse_data(Sigma, loopNum=20):

    Sig2 = Sigma**2
    SigmaSum = sum(Sig2)
    for i in range(loopNum):
        SigmaI = sum(Sig2[:i+1])
        print 'primary: %s, accumulate: %s%%' % (format(i+1, '2.0f'), format(SigmaI/SigmaSum*100, '4.2f'))



def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split() for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return datArr


def rebuild(u, sigma, v, per=0.9):
    m = len(u)
    n = len(v)
    a = np.zeros((m, n))
    sigma_sum = int(sum(sigma))
    cur_sum = 0
    k = 0
    while cur_sum <= sigma_sum * per:
        uk = u[:, k].reshape(m, 1)
        vk = v[k].reshape(1, n)

        a += sigma[k] * np.dot(uk, vk)

        cur_sum += sigma[k] 
        k += 1
    a[a < 0] = 0
    a[a > 255] = 255
    print("k/n==%d/%d==%.2f" % (k, n, k / n))
    return np.rint(a).astype("uint8")

if __name__ == "__main__":
    #dataMat = loadDataSet('/home/luo//Luo/PCA/MachineLearning/input/13.PCA/testSet.txt')
    filename=sys.argv[1]
    dataMat = loadDataSet(filename)



    
    u, sigma, v = np.linalg.svd(dataMat)
    #print "u: ",  np.shape(u)
    #print "sigma: ", np.shape(sigma)
    #print "v: ", np.shape(v)

    k=230
    reconMat = rebuild2(u, sigma, v,k)
    m=np.shape(dataMat)[0]
    n=np.shape(dataMat)[1]
    print m,n
    print "%f" % (float((m*n))/float((m*k)+k*k+(k*n)))
    sum_temp=0

    for i in range (m):
        for j in range (n):
               # print dataMat[i][j]
               # print reconMat[i][j]
                #float(pic_recon[i][j])
                #float(new[i][j])
                sum_temp+=(float(dataMat[i][j])-float(reconMat[i][j]))**2
     
    rmse=(sum_temp/n)**0.5

    print(rmse)
#analyse_data(sigma,6)

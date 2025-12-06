import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler    # 数据标准化
from scipy.stats import bartlett    # bartlett球形检验
import math as math

data = pd.read_csv(r'C:\Users\delapi\2019年主要城市空气质量数据.csv', encoding='GB18030')
def kmo(dataset_corr):
    corr_inv = np.linalg.inv(dataset_corr)
    nrow_inv_corr, ncol_inv_corr = dataset_corr.shape
    A = np.ones((nrow_inv_corr, ncol_inv_corr))
    for i in range(0, nrow_inv_corr):
        for j in range(i, ncol_inv_corr):
            A[i, j] = -(corr_inv[i, j]) / (math.sqrt(corr_inv[i, i] * corr_inv[j, j]))
            A[j, i] = A[i, j]
    dataset_corr = np.asarray(dataset_corr)
    kmo_num = np.sum(np.square(dataset_corr)) - np.sum(np.square(np.diagonal(A)))
    kmo_denom = kmo_num + np.sum(np.square(A)) - np.sum(np.square(np.diagonal(A)))
    kmo_value = kmo_num / kmo_denom
    return kmo_value
# 提取X
X = data.iloc[:, 1:]
# 计算相关系数
cor = X.corr()
# KMO检验
print('KMO测度:', kmo(cor))
# Bartlett球形检验
cor = cor.values
print(bartlett(cor[0], cor[1], cor[2], cor[3], cor[4], cor[5]))
X1 = StandardScaler().fit_transform(X)   # 先对X进行标准化
X_cov = np.cov(X1.T) # 计算协方差矩阵
eigValues, eigVectors = np.linalg.eig(X_cov)

# k:表示提取前k个特征值对应的特征向量
def pea(k):
    index = eigValues.argsort()[-k:][::-1]  # 选取前k个特征值以及所对应的特征向量
    topk_eigVec = eigVectors[:, index]
    topk_eigVal = eigValues[index]
    # 计算方差贡献率和累计方差贡献率
    gxl = []    # 用来存放贡献率
    print(topk_eigVal.tolist())
    for vec in topk_eigVal.tolist():
        gxl.append(vec / sum(eigValues.tolist()))
    lj_gxl = [] # 用来存放累计贡献率
    for i in range(len(gxl)):
        lj = sum(gxl[:i+1])
        lj_gxl.append(lj)
    return topk_eigVal, topk_eigVec, gxl, lj_gxl
val, vec, gxl, lj_gxl = pea(6)  # 提取全部的特征值和特征向量（已排好序）
print('方差贡献率：', [round(x, 2) for x in gxl])   #加round()是保留小数点后两位
print()
print('累计方差贡献率：', [round(x, 2) for x in lj_gxl])

# 因子载荷矩阵就是投影后的数据y与原始数据x之间的相关系数
# X为原始数据，topk_eigVec为筛选出的前k个特征向量
def get_factor_coefficient(X, topk_eigVec):
    X_columns = X.columns
    X = pd.DataFrame(X1, columns=X_columns)
    row, col = topk_eigVec.shape
    columns = []    # 用来存放指定列名
    for i in range(col):
        column = 'y' + str(i + 1)
        columns.append(column)
    # 计算因子载荷矩阵
    Y = X.dot(topk_eigVec)
    factor_mat = pd.concat([X, Y], axis=1).corr()
    factor_mat = factor_mat.iloc[:row, row:]    # 只需提取对角线上的相关系数
    factor_mat.columns = columns
    # 计算各指标系数
    columns = []    # 用来存放指定列名
    for i in range(col):
        col = '第' + str(i + 1) + '个主成分' + 'y' + str(i + 1) + '的系数'
        columns.append(col)
    coefficient = pd.DataFrame(topk_eigVec, columns=columns, index=X_columns)
    return factor_mat, coefficient
# 提取前3个特征向量
top3Vec = vec[:, :3]
factor_mat, coefficient = get_factor_coefficient(X, top3Vec)
print(factor_mat)
print(coefficient)

# topk_eigVec为筛选出的前k个特征向量
# gxl为由前k个特征值所计算的贡献率
def get_score(topk_eigVec, gxl):
    Y = X1.dot(topk_eigVec)
    Score = np.array(gxl).dot(Y.T)
    return Score
top3Gxl = gxl[:3]
print(top3Gxl)
score = get_score(top3Vec, top3Gxl)
print(score)

def indicator_weight(eig_vals, eig_vecs, n_components): # 计算各原始指标的综合权重（基于前n个主成分）
    # 主成分权重（特征值占比）
    pc_weights = eig_vals[:n_components] / sum(eig_vals[:n_components])
    # 特征向量标准化
    eig_vecs_norm = eig_vecs[:, :n_components] / np.linalg.norm(eig_vecs[:, :n_components], axis=0)
    # 综合权重 = 主成分权重 * 特征向量 求和，再归一化
    weight = np.dot(eig_vecs_norm, pc_weights)
    weight = weight / sum(weight)   # 归一化到总和为一
    weight_df = pd.Series(weight, index = X.columns, name='指标权重')
    return weight_df

# 计算指标权重
top3Val = val[:3]
weight_df = indicator_weight(eigValues, eigVectors, 3)
print('\n' + '=' * 60)
print('6.各指标综合权重（降序）')
print(weight_df.sort_values(ascending=False).round(4))
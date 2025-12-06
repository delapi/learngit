import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler    # 数据标准化
from scipy.stats import bartlett    # bartlett球形检验
import math as math

data = pd.read_csv(r'C:\Users\delapi\2019年我国31个省市居民家庭人均主要食品消费量.csv', encoding='GB18030')
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
province_names = data.iloc[:, 0]    # 提取省市名称
# 计算相关系数
cor = X.corr()
# KMO检验
print('KMO测度:', kmo(cor))
# Bartlett球形检验
cor = cor.values
print(bartlett(cor[0], cor[1], cor[2], cor[3], cor[4], cor[5], cor[6], cor[7], cor[8],\
      cor[9]))
X1 = StandardScaler().fit_transform(X)   # 先对X进行标准化
X_cov = np.cov(X1.T) # 计算协方差矩阵
eigValues, eigVectors = np.linalg.eig(X_cov) 

# X:输入的样本  k:表示提取前k个特征值对应的特征向量
def pea(X, k):
    X = StandardScaler().fit_transform(X)   # 先对X进行标准化
    X_cov = np.cov(X.T) # 计算协方差矩阵
    eigValues, eigVectors = np.linalg.eig(X_cov)    # 计算特征值和特征向量
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
val, vec, gxl, lj_gxl = pea(X, 10)  # 提取全部的特征值和特征向量（已排好序）
print('方差贡献率：', [round(x, 2) for x in gxl])   #加round()是保留小数点后两位
print()
print('累计方差贡献率：', [round(x, 2) for x in lj_gxl])

# 因子载荷矩阵就是投影后的数据y与原始数据x之间的相关系数
# X为原始数据，topk_eigVec为筛选出的前k个特征向量
def get_factor_coefficient(X, topk_eigVec):
    X_columns = X.columns
    X = StandardScaler().fit_transform(X)
    X = pd.DataFrame(X, columns=X_columns)
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
# 提取前4个特征向量
top4Vec = vec[:, :4]
factor_mat, coefficient = get_factor_coefficient(X, top4Vec)
print(factor_mat)
print(coefficient)

# X为原始数据
# topk_eigVec为筛选出的前k个特征向量
# gxl为由前k个特征值所计算的贡献率
def get_score(X, topk_eigVec, gxl):
    X = StandardScaler().fit_transform(X)
    Y = X.dot(topk_eigVec)
    Score = np.array(gxl).dot(Y.T)
    return Score
top4Gxl = gxl[:4]
print(top4Gxl)
score = get_score(X, top4Vec, top4Gxl)
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
top4Val = val[:4]
weight_df = indicator_weight(eigValues, eigVectors, 4)
print('\n' + '=' * 60)
print('6.各指标综合权重（降序）')
print(weight_df.sort_values(ascending=False).round(4))

indicator_groups = {
    '主食类':['粮食'],
    '糖油类':['食糖', '食用油'],
    '奶蛋类':['奶类', '蛋类'],
    '肉类':['肉类', '禽类', '水产品'],
    '果蔬类':['干鲜瓜果类', '蔬菜及食用菌']
}
# 步骤1：检验分组指标
for group, indicators in indicator_groups.items():
    invalid_inds = [ind for ind in indicators if ind not in X.columns]
    if invalid_inds:
        print(f'\n警告:{group}中的{invalid_inds}不在数据列中，请检查！')

# 步骤2：计算类别权重（组内指标权重求和——归一化）
category_weights = {}
for group, indicators in indicator_groups.items():
    group_weight = weight_df[indicators].sum()  # 组内指标权重求和
    category_weights[group] = group_weight
category_weights = pd.Series(category_weights, name='类别权重')
category_weights = category_weights / category_weights.sum()    # 归一化
print('\n' + '=' * 60)
print('7.类别权重（主管分组，归一化后）')
print(category_weights.round(4))

# 步骤3：计算各省市的类别得分（两种方式可选：等权重/加权）
def calculate_category_score(X_std_df, indicator_groups, weight_df, method = 'weighted'):
    '''
 
    :param X_std_df: 标准化数据（带列名）
    :param indicator_groups: 主观分组
    :param weight_df: 指标权重
    :param method: equal（等权均值）/weighted（指标权重加权）
    :return: 省市类别得分
    '''
    category_scores = {}
    for group, indicators in indicator_groups.items():
        group_data = X_std_df[indicators]   # 组内指标标准化数据
        if method == 'equal':
            # 方式1：等权均值
            score = group_data.mean(axis = 1)
        else:
            # 方式2：按指标权重加权
            group_w = weight_df[indicators]
            group_w = group_w / group_w.sum()   # 组内权重归一化
            score = group_data.dot(group_w)
        category_scores[group] = score
    return pd.DataFrame(category_scores)

# 标准化数据转为DataFrame（带列名和省市索引）
X_std_df = pd.DataFrame(X1, index=province_names, columns=X.columns)

# 计算类别得分（默认加权，如需等权改为method=‘equal’）
category_score_df = calculate_category_score(X_std_df, indicator_groups, weight_df)

# 输出省市类别得分
print('\n' + '=' * 60)
print('8.各省市类别得分（标准化后，越高代表该类别消费水平越高）')
print(category_score_df.round(4))

# 可选：输出某类别的TOP10
print('\n' + '=' * 60)
print('9.奶蛋类得分TOP10')
print(category_score_df['奶蛋类'].sort_values(ascending = False).head(10).round(4))
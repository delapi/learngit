import numpy as np  # 数学基础库
import pandas as pd # 基本数据处理工具
from sklearn.preprocessing import StandardScaler    # 数据标准化模块
from factor_analyzer import factor_analyzer, Rotator, FactorAnalyzer    # factor_analyzer需单独加载
import math #数学运算模块
import matplotlib.pyplot as plt # 画图模块
from IPython.display import display
import prince   # 做对应分析的程序包

mydata = pd.read_csv(r'C:\Users\delapi\2019年我国我国31个省市经济指标相关数据.csv', encoding='GB18030')   # 按指定路径读取数据
print(mydata)   # 查看数据
data_index = mydata['地区']   # 删除指定的定性变量
del mydata['地区']
sc = StandardScaler()   # 用z-score进行数据标准化
sc = (sc.fit_transform(mydata)) # 把数据转换成数据框格式
sc_data = pd.DataFrame(sc, index=data_index, columns=['国内生产总值', '居民消费水平', '固定资产投资',\
'职工平均工资', '货物周转量', '居民消费价格指数', '商品零售价格指数', '工业总产值'])
display(sc_data)    # 查看标准化后的数据

mydata1 = sc_data.copy()   # 数据赋值
mydata1_corr = mydata1.corr()   # 计算相关矩阵
display('\n相关系数：\n', mydata1_corr) # 显示相关矩阵
cmap = plt.get_cmap('Blues')    # 以下绘制相关矩阵的热力图
fig = plt.figure()
ax = fig.add_subplot(111)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
map = ax.imshow(mydata1_corr, interpolation='nearest', cmap=cmap, vmin=0, vmax=1)
plt.title('correlation coefficient - - headmap')
ax.set_yticks(range(len(mydata1_corr.columns))) # Y轴尺度
ax.set_yticklabels(mydata1_corr.columns)    # Y轴标签
ax.set_xticks(range(len(mydata1_corr))) # X轴尺度
ax.set_xticklabels(mydata1_corr.columns, rotation = 45) # X轴标签
plt.colorbar(map)
plt.show()

def kmo(dataset_corr):
    corr_inv = np.linalg.inv(dataset_corr)
    nrow_inv_corr, ncol_inv_corr = dataset_corr.shape
    A = np.ones((nrow_inv_corr, ncol_inv_corr))
    for i in range(0, nrow_inv_corr, 1):
        for j in range(i, ncol_inv_corr, 1):
            A[i, j] = -(corr_inv[i, j]) / (math.sqrt(corr_inv[i, i] * corr_inv[j, j]))
            A[j, i] = A[i, j]
    dataset_corr = np.asarray(dataset_corr)
    kmo_num = np.sum(np.square(dataset_corr)) - np.sum(np.square(np.diagonal(A)))
    kmo_denom = kmo_num + np.sum(np.square(A)) - np.sum(np.square(np.diagonal(A)))
    kmo_value = kmo_num / kmo_denom
    return kmo_value
print('\nKMO测度：', kmo(mydata1_corr))

eig_value, eigvecotr = np.linalg.eig(mydata1_corr)  # 计算相关矩阵的特征值、特征向量
eig = pd.DataFrame()
eig['eig_value'] = eig_value
eig.sort_values('eig_value', ascending=False, inplace=True)    # 特征值排序
display('\n特征值\n:', eig)
eig1 = pd.DataFrame(eigvecotr)
eig1.index = mydata1_corr.columns
display('\n特征向量\n', eig1)   # 特征向量矩阵
for m in range(0, 8):   # 输出公因子个数
    if eig['eig_value'][:m].sum() / eig['eig_value'].sum() >= 0.85:
        print('\n公因子个数：', m)
        break

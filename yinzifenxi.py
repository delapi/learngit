import numpy as np  # 数学基础库
import pandas as pd # 基本数据处理工具
from sklearn.preprocessing import StandardScaler    # 数据标准化模块
from factor_analyzer import factor_analyzer, Rotator, FactorAnalyzer    # factor_analyzer需单独加载
import math #数学运算模块
import matplotlib.pyplot as plt # 画图模块
from IPython.display import display
import prince   # 做对应分析的程序包

mydata = pd.read_csv(r'C:\Users\delapi\2019年我国居民消费支出.csv', encoding='GB18030')   # 按指定路径读取数据
print(mydata)   # 查看数据
data_index = mydata['地区']   # 删除指定的定性变量
del mydata['地区']
sc = StandardScaler()   # 用z-score进行数据标准化
sc = (sc.fit_transform(mydata)) # 把数据转换成数据框格式
sc_data = pd.DataFrame(sc, index=data_index, columns=['公共服务支出', '国防支出', '公共安全支出',\
'教育支出', '科学技术支出', '文体传媒支出', '保障就业支出', '卫生健康支出', '节能环保支出',\
'城乡社区支出', '农林水支出', '交通运输支出', '其他支出'])
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
for m in range(0, 13):   # 输出公因子个数
    if eig['eig_value'][:m].sum() / eig['eig_value'].sum() >= 0.85:
        print('\n公因子个数：', m)
        break
A = np.matrix(np.zeros((13, 3))) # 计算因子载荷矩阵
i = 0; j = 0
while i < 3:
    j = 0
    while j < 13:
        A[j: , i] = math.sqrt(eig_value[i]) * eigvecotr[j, i]
        j = j + 1
    i = i + 1
a = pd.DataFrame(A)
a.columns = ['factor1', 'factor2', 'factor3']
a.index = mydata1_corr.columns
display('\n因子载荷阵\n', a)
fa = FactorAnalyzer(n_factors=3, method='principal', rotation='varimax')    # 因子分析
fa.loadings_ = a
var = fa.get_factor_variance()  # 贡献率
var1 = pd.DataFrame()
var1['方差'] = list(var)[0]
var1['贡献率'] = list(var)[1]
var1['累计贡献率'] = list(var)[2]
display(var1)

rotator = Rotator()
b = pd.DataFrame(rotator.fit_transform(fa.loadings_))
b.columns = ['factor1', 'factor2', 'factor3']
b.index = mydata1_corr.columns
display('\n因子旋转：\n', b)

X1 = np.matrix(mydata1_corr)
X1 = np.linalg.inv(X1)
b = np.matrix(b)
factor_score = np.dot(X1, b)
factor_score = pd.DataFrame(factor_score)
factor_score.columns = ['factor1', 'factor2', 'factor3']
display('\n因子得分系数矩阵：\n', factor_score)
fa_t_score = np.dot(np.matrix(mydata1), np.matrix(factor_score))
fa_t_score = pd.DataFrame(fa_t_score, columns=['factor1得分', 'factor2得分', 'factor3得分'])
fa_t_score.index = (data_index)
c = [[0.702494], [0.091526], [0.078303]]    # 输入公共因子的方差贡献率
score = np.dot(fa_t_score, c) / 0.872323
fa_t_score['综合得分'] = score
display('\n因子得分：\n', fa_t_score)

data = sc_data  # 读取标准化后的数据
ca = prince.CA( # 对数据进行对应分析
n_components=3,
n_iter=100,
copy=True,
check_input=True,
engine='sklearn',
random_state=42)
df = pd.DataFrame(data)
data2 = (df + 2).copy() # 因其数据小于0，所有值都加上一个常数使其均大于0
data2.columns.rename('支出变量', inplace=True)  # 重命名
data2.index.rename('地区', inplace=True)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
ca = ca.fit(data2)
row_coords = ca.row_coordinates(data2)  # 行坐标
col_coords = ca.column_coordinates(data2)   # 列坐标
fig, ax = plt.subplots(figsize = (9, 7))    # 手动创建画布
# 绘制行点+标签
ax.scatter(row_coords[0], row_coords[1], s=100, c='red', alpha=0.8, label = '地区')
for idx in row_coords.index:
    ax.text(row_coords.loc[idx, 0] + 0.02, row_coords.loc[idx, 1] + 0.02, idx, fontsize = 8, color = 'red')
# 绘制列点+标签
ax.scatter(col_coords[0], col_coords[1], s=100, c='blue', alpha=0.8, label = '支出变量')
for idx in col_coords.index:
    ax.text(col_coords.loc[idx, 0] + 0.02, col_coords.loc[idx, 1] + 0.02, idx, fontsize = 8, color = 'blue')
ax.axhline(y=0, color = 'gray', linestyle = '--', alpha = 0.5)
ax.axvline(x=0, color = 'gray', linestyle = '--', alpha = 0.5)
ax.legend()
plt.tight_layout()
plt.show()
'''
auth:canhun
'''
import numpy as np
import pandas as pd
url = '''https://mp.weixin.qq.com/s?__biz=MjM5MDI1ODUyMA==&mid=2672942422&idx=2&sn=1ad0ab44fa3e13346d80e9011cc7d925&chksm=bce2f9618b9570774a4aea0500a8fa96fa9a178d3996e64b9c2342d1f357be3b15fb11d4f662&mpshare=1&scene=23&srcid=01050tJzz67m8SJ8yJhTuEDt#rd'''

# 数据读取
# df = pd.read_json('../a.json')
'''1.创建数据框'''
df = pd.DataFrame({
                   "id":[1001,1002,1003,1004,1005,1006],
                   "date":pd.date_range('20130102', periods=6),
                   "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
                   "age":[23,44,54,32,34,32],
                   "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
                   "price":[1200,np.nan,2133,5433,np.nan,4432]
                   },
                   columns =['id','date','city','category','age','price'])
# print(df)

'''2.数据框检查'''
# 2.1查看数据框行列
rowsNum_columsNum = df.shape   # rowsNum_columsNum=(6,6)  --返回元组 (6,6,)6行 6列

#2.2 #数据表信息
# df.info()
# 显示数据表信息 返回none

#2.3 查看数据表各列格式
colums_types = df.dtypes
# print(colums_types)
#查看某列格式
colum_type = df['id'].dtype
# print(colum_type)

#2.4 判断空值     常用于空值处理
# 是空值返回True 非空返回False type:bool
#整个数据框判断为空
df.isnull()  #
#整列判断为空
df['price'].isnull()
# print(df['price'].isnull())
# for i in df['price'].isnull():
#     print(i)

#2.5 查看唯一值
df['city'].unique()  #返回数组对象

#2.6 查看数据表的值
df.values

#2.7 查看列名称
df.columns

#2.8 查看前3行数据
df.head(3)
#查看后三行数据
df.tail(3)

'''3.数据表清洗'''
#3.1 处理空值(删除或填充)

#删除数据表中含有空值的行
df.dropna(how='any')
#使用数字0填充数据表中空值
df.fillna(value=0)
#使用price均值对NA进行填充
df['price'].fillna(df['price'].mean())
df['price'] = df['price'].fillna(df['price'].mean())
#3.2 清理空格
#清除city字段中的字符空格
df['city']=df['city'].map(str.strip)

#3.3 大小写转换
#city列大小写转换  upper/lower
df['city']=df['city'].str.upper()

#3.4 更改数据格式
#更改数据格式
df['price'] = df['price'].astype('int')

#3.5 更改列名称
df = df.rename(columns={'category':'category-size'})

#3.6 删除重复值   drop_duplicates函数删除重复值。
#删除后出现的重复值
df['city'].drop_duplicates()
#删除先出现的重复值
df['city'].drop_duplicates(keep='last')

#3.7 数值修改及替换
df['city'] = df['city'].replace('sh', 'shanghai')

#3.8 删除行列 数据
df = df.drop(columns=['category',])  # 删除category列
df = df.drop([0, 1])                  # 删除索引为 0 和1 的行

'''4.数据合并'''
df1 = pd.DataFrame({
                    'id':[1001,1002,1003,1004,1005,1006,1007,1008],
                    'gender':['male','female','male','female','male','female','male','female'],
                    'pay':['Y','N','Y','Y','N','Y','N','Y',],
                    'm-point':[10,12,20,40,40,40,30,20]
                    })
#4.1数据表匹配合并
df_inner = pd.merge(df,df1,how='inner') #内连接
df_left = pd.merge(df,df1,how='left')   #左连接
df_right = pd.merge(df,df1,how='right') #右连接
df_outer = pd.merge(df,df1,how='outer') #完全连接
# 两表关联字段名不一致时使用
df2 = df1.rename(columns={'id':'id1'})
df_other = df.merge(df2, left_on='id', right_on='id1', how='outer')  #多个字段关联是 left on  和right on 的值写入一个list,顺序相同

# 4.2 设置索引列
df_inner.set_index('id')

# 4.3 按特定列的值排序
df_inner.sort_values(by=['age'])  #多个字段进行排序
#按索引列排序
df_inner.sort_index()

# 4.4 数据分组
df_inner['group'] = np.where(df_inner['price']>3000,'expensive','cheap')
#对复合多个条件的数据进行分组标记
df_inner.loc[(df_inner['city'] == 'beijing') & (df_inner['price'] >= 4000), 'sign'] = 'mark'

#4.5 数据分列
df_split = pd.DataFrame([x.split('-') for x in df['category']],index=df.index,columns=['category','size']) # 先将字段分成两列,组成数据框
df = df.merge(df_split,right_index=True, left_index=True)

'''5.数据提取'''

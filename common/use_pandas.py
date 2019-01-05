'''
auth:canhun
'''
import numpy as np
import pandas as pd
'''https://mp.weixin.qq.com/s?__biz=MjM5MDI1ODUyMA==&mid=2672942422&idx=2&sn=1ad0ab44fa3e13346d80e9011cc7d925&chksm=bce2f9618b9570774a4aea0500a8fa96fa9a178d3996e64b9c2342d1f357be3b15fb11d4f662&mpshare=1&scene=23&srcid=01050tJzz67m8SJ8yJhTuEDt#rd'''

# 数据读取
# df = pd.DataFrame(pd.read_json('../a.json'))
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
# 2.1查看数据框行列 --返回元组 (6,6,)6行 6列
rowsNum_columsNum = df.shape

#2.2 #数据表信息
tab_info = df.info()
print(tab_info)
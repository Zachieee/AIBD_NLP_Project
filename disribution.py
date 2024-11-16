import pandas as pd
import numpy as np

data = pd.read_csv('Data/news.csv')
# print(data['category'])
df = pd.DataFrame(data)

# 使用value_counts()统计每个类别的分布情况
category_distribution = df['category'].value_counts()

# 打印结果
print(category_distribution)
category_distribution.to_csv('Data/distribution.csv')

# 确保日期字段是datetime类型
data['date'] = pd.to_datetime(data['date'])

# 可以按年、月、日等不同时间粒度进行分组
data['year_month'] = data['date'].dt.to_period('M')

# 按类别和月份分组，计算每个类别在每个月的计数
monthly_distribution = data.groupby(['category', 'year_month']).size().reset_index(name='count')

# 打印结果
print(monthly_distribution)

# 如果需要，可以将结果保存为CSV文件
monthly_distribution.to_csv('Data/monthly_distribution.csv', index=False)
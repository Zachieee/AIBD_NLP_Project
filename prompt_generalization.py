import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

# 假设数据已经加载到DataFrame中
data = pd.read_csv('Data/monthly_distribution.csv')

# 确保日期字段是datetime类型，并去除时间部分，只保留日期
data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m').dt.date

# 统计每个类别的样本量
category_counts = data.groupby(['category', 'year_month']).size().unstack(fill_value=0)

# 定义一个函数来生成多元化的任务
def generate_diversified_tasks(category, start_date, end_date, count):
    tasks = []
    # 计算整个DataFrame的平均值
    overall_mean = category_counts.mean().mean()
    num_prompts = min(int(count / overall_mean * 2), 2)  # 根据样本量调整prompt数量，最多2条
    task_templates = [
        "Summarize the key events in {category} from {time_period_start} to {time_period_end}.",
        "Predict the future trends in {category} based on the data from {time_period_start} to {time_period_end}.",
        "Compare the {category} data between {time_period_start} and {time_period_end}.",
        "Analyze the impact of significant events on {category} from {time_period_start} to {time_period_end}."
    ]
    for _ in range(num_prompts):
        prompt_template = np.random.choice(task_templates)
        task = prompt_template.format(category=category, time_period_start=start_date, time_period_end=end_date)
        tasks.append(task)
    return tasks

# 根据数据分布生成时间段和prompts
prompts = []
# 只选择样本量最高的10个时间段
top_categories = category_counts.sum(axis=1).sort_values(ascending=False).head(10).index
for category in top_categories:
    counts = category_counts.loc[category]
    sorted_counts = counts.sort_values(ascending=False)
    top_times = sorted_counts.head(5).index.tolist()  # 取样本量最高的5个时间段
    for start_date in top_times:
        # 确保时间段至少覆盖半个月
        end_date = start_date + relativedelta(months=1) if (start_date + relativedelta(months=1)) in counts.index else start_date + relativedelta(days=15)
        # 确保end_date在数据范围内
        if end_date in counts.index:
            count = counts.loc[start_date:end_date].sum()
            if count > 0:  # 只考虑有数据的时间段
                time_prompts = generate_diversified_tasks(category, start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m'), count)
                prompts.extend(time_prompts)

# 输出10条最优质的prompts
best_prompts = sorted(prompts, key=lambda x: prompts.count(x), reverse=True)[:20]
for prompt in best_prompts:
    print(prompt)
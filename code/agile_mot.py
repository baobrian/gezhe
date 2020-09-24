# coding=utf-8

import pandas as pd
import os
import cohort_anlysis as CAS
import datetime
import time
import numpy as np
file_path='E:\Data_temp\\20200102\data\\'
save_path='E:\Data_temp\\20200102\\result'
files = os.listdir(file_path)
data = pd.read_csv(file_path + files[0])
os.chdir(save_path)
columns=data.columns
# 计算漏斗转化及阶段漏斗转化
# 漏斗环节转化率： 本环节用户数/上一环节用户数
# 阶段转化率   ：  本环节用户数/第一环节用户基数

values= [sum(data[columns[i+1]].notnull()) for i in range(1,5)]
cc=columns.values[2:6].tolist()
transform_df=pd.DataFrame(data=np.array(values).reshape(4,1),index=columns.values[2:6],columns=['value'])
transform_df.to_csv('transform.csv')

print '漏斗转化各个阶段的数据计算已经完成'

# 开始节点MOT转化时机/转化成效
# for i in range(1,4):
#     result_final_day,result_final_hour,result_final_min=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
#     result_timing_day,result_timing_hour,result_timing_min=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
#     start_pk=columns[i+1]
#     end_pk=columns[i+2]
#     print  sum(data[start_pk].notnull())
#     data=data[data[start_pk].notnull()]
#     cohort_final=CAS.CohortAnalysis(data=data,stat_time=start_pk,end_time='draw_appl',boundary=30)
#     cohort_timing=CAS.CohortAnalysis(data=data,stat_time=start_pk,end_time=end_pk,boundary=30)
#     # 计算最终转化时机 ：(不同时机) 最终环节用户数/上一环节用户数(维度：天、时、分)
#     result_final_day=cohort_final.analysis_cohort_day()
#     result_final_hour = cohort_final.analysis_cohort_hour()
#     result_final_min= cohort_final.analysis_cohort_minute()
#
#     result_final_day.to_csv('final_day_'+start_pk+'.csv')
#     result_final_hour.to_csv('final_hour_' + start_pk + '.csv')
#     result_final_min.to_csv('final_min_' + start_pk + '.csv')
#     # 计算环节转化时机 ：(不同时机)本环节用户数/上一环节用户数(维度：天、时、分)
#     result_timing_day=cohort_timing.analysis_cohort_day()
#     result_timing_hour=cohort_timing.analysis_cohort_hour()
#     result_timing_min=cohort_timing.analysis_cohort_minute()
#
#     result_timing_day.to_csv('timing_day_'+start_pk+'.csv')
#     result_timing_hour.to_csv('timing_hour_' + start_pk + '.csv')
#     result_timing_min.to_csv('timing_min_' + start_pk + '.csv')
# print '节点MOT转化时机分析已完成'




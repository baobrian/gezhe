# coding=utf-8
import pandas as pd
import os
import cohort_anlysis as CAS
import datetime


# 读取数据
date = '20191129'
path = './data/'
file_save_path = './result/'
files = os.listdir(path)
# data=pd.read_csv(path+files[0],index_col=0)
data = pd.read_csv(path + files[0])
data.info()

print '实名异常对数据为%s'   % sum((pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['tname_tm'].str[0:20])))

print '额度申请异常对数据为%s'   % sum((pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['limit_crt_dt'].str[0:20])))

gg=data[pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['limit_crt_dt'].str[0:20])]

print '额度流程结束异常对数据为%s'   % sum((pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['limit_wfi_end_tm'].str[0:20])))

hh=data[pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['limit_wfi_end_tm'].str[0:20])]


print '提款申请异常对数据为%s'   % sum((pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['draw_crt_dt'].str[0:20])))

jj=data[pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['draw_crt_dt'].str[0:20])]


print '提款流程结束异常对数据为%s'   % sum((pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['draw_wfi_end_tm'].str[0:20])))



kk=data[pd.to_datetime(data['app_down_tm'].str[0:20])\
                            >pd.to_datetime(data['draw_wfi_end_tm'].str[0:20])]
pass
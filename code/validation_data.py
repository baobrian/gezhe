# coding=utf-8

import pandas as pd
import os
import datetime


# 读取数据
date = '20200220'


path = 'E:\Data_temp\\'+date+'\\result\\'
# cust_file_save_path = 'E:\Data_temp\\'+date+'\\custresult\\'
# shenpi_file_save_path = 'E:\Data_temp\\'+date+'\\shenpiresult\\'
# redraw_file_save_path = 'E:\Data_temp\\'+date+'\\redrawresult\\'

start_date=datetime.datetime(2020,2,19,0,0,0)
unit=datetime.timedelta(hours=24)
files = os.listdir(path)
data = pd.read_csv(path + files[0])

data=data[(data['rgst_src'] != 'YXD')\
                  &(data['is_yxd'] != '04C')\
                  &(data['whlist_ind'] != 1)\
                  &(data['loan_prom'].isnull()) \
          & (pd.to_datetime(data['app_down_tm']) >= start_date) \
          & (pd.to_datetime(data['app_down_tm']) < start_date + 1 * unit)
]
print data.shape[0]

print data.groupby(['rgst_src']).size()
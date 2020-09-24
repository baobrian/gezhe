# coding=utf-8

import pandas as pd
import numpy as np
import os



def contact_data(data_path=None):
    files = os.listdir(file_path)
    result = pd.DataFrame()
    for file in files:
        result = result.append(pd.read_csv(file_path + file))
        # print result.shape
    result['rank']=np.arange(0,result.shape[0])
    result.set_index(['rank'], inplace=True)
    print ('已合并完数据,数据一共有%s条' %result.shape[0])
    return result



if __name__ == '__main__':
    file_path='E:\Data_temp\\20200220\data\\'
    save_path='E:\Data_temp\\20200220\\result\\'
    os.chdir(save_path)
    result=contact_data(data_path=file_path)
    result.to_csv('yiqing_all.csv')
    print ('data contact over!')





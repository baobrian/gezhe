# coding=utf-8
import pandas as pd
import os
import cohort_anlysis as CAS
import datetime
import time

begin= time.time()
def fliter_data(data=None,product='tongyong_jing'):
    '''
    :param data:待筛选的数据
    :param product: 产品对应的名称
    :return: 筛选完的数据
    '''
    print ('data一共有%s条数据' %data.shape[0])
    if product=='tongyong_jing':
        condition=(data['rgst_src'] != 'YXD')\
                  &(data['is_yxd'] != '04C')\
                  &(data['whlist_ind'] != 1)\
                  &(data['loan_prom'].isnull())
    if product=='yxd':
        condition=(data['rgst_src']!='YXD')\
                   &(data['is_yxd']=='04C') \
                   &(data['whlist_ind'] != 1)

    if product=='white_jing':
        condition=(data['rgst_src']!='YXD')\
                  &(data['is_yxd']!='04C')\
                  &(data['whlist_ind']==1)\
                  &(data['loan_prom'].isnull())

    print ('%s产品一共包含数据%d条!' %(product,condition.sum()))
    # return data[condition]
    return data[condition\
                &(pd.to_datetime(data['app_down_tm'])>=start_date)\
                &(pd.to_datetime(data['app_down_tm'])<=start_date+60*unit)]


# 读取数据
date = '20200220'
path = 'E:\Data_temp\\'+date+'\\result\\'
cust_file_save_path = 'E:\Data_temp\\'+date+'\\custresult\\'
shenpi_file_save_path = 'E:\Data_temp\\'+date+'\\shenpiresult\\'
redraw_file_save_path = 'E:\Data_temp\\'+date+'\\redrawresult\\'
files = os.listdir(path)
data = pd.read_csv(path + files[0])
# print '专案的数据%s'% data['loan_prom'].notnull().sum()
# print '复提的数据%s'% (data['draw_cnt']==2).sum()
'''
客户生命周期的不同节点:包含实名(real_name)，额度申请(limit_appl)，提款申请(draw_appl)，复提申请(redraw_appl)
审批周期不同节点：额度通过(limit_pass)，提款通过(draw_pass)，复提通过(redraw_pass)
'''
cust_node_list=[
                'real_name',
                'limit_appl',
                'draw_appl',
                 # 'redraw_appl'
                ]
shenpi_node_list=['limit_pass','draw_pass']

redraw_node_list=['redraw_appl','redraw_pass']

node_dict = { 'real_name':   ['app_down_tm','tname_tm'],\
              'limit_appl':  ['tname_tm','limit_crt_dt'], \
              'limit_pass':  ['limit_wfi_start_tm', 'limit_wfi_end_tm','limit_apprv_sts'],\
              'draw_appl':   ['limit_wfi_end_tm','draw_wfi_start_tm','limit_apprv_sts'], \
              'draw_pass':   ['draw_wfi_start_tm','draw_wfi_end_tm','draw_apprv_sts'],\
              'redraw_appl': ['user_id','draw_wfi_end_tm_left','draw_wfi_start_tm_right','draw_apprv_sts_left'],\
              'redraw_pass': ['user_id','draw_wfi_start_tm_right','draw_wfi_end_tm_right','draw_apprv_sts_right']
             }

'''
产品主要分为三类：精英贷白名单，精英贷非白名单，永享贷
'''
# products=['tongyong_jing','white_jing','yxd']
products=['tongyong_jing']
# 统计的数据的开始日期,
start_date=datetime.datetime(2020,1,1,0,0,0)
unit=datetime.timedelta(hours=24)
# 计算客户节点转化
for product in products:
    df=fliter_data(data=data,product=product)
    print (df.shape[0])
    print ('复提数据一共有%s' %sum(df['draw_cnt']!=2))
    uniqe_df=df[df['draw_cnt']!=2]
    print ('%s产品去除复提的数据一共有数据%d条' % (product, uniqe_df.shape[0]))
    for node in cust_node_list:
        result=pd.DataFrame()
        pk=node_dict[node]
        temp_df=uniqe_df[(uniqe_df[pk[0]].notnull())\
                         &(pd.to_datetime(uniqe_df[pk[0]])>=start_date)\
                         &(pd.to_datetime(uniqe_df[pk[0]])<start_date+60*unit)\
                        ]
        if node=='draw_appl':
            temp_df=temp_df[temp_df['limit_apprv_sts']==997]
        cohort=CAS.CohortAnalysis(data=temp_df,stat_time=pk[0],end_time=pk[1],boundary=7)
        result=result.append(cohort.analysis_cohort_day(isPercent=False))
        result.to_csv(cust_file_save_path+'result_' +product+'_'+node + '.csv', header=True)

# 计算审批节点转化
# for product in products:
#     df=fliter_data(data=data,product=product)
#     uniqe_df=df[df['draw_cnt']!=2]
#     print '%s产品去除复提的数据一共有数据%d条' %(product,uniqe_df.shape[0])
#     for node in shenpi_node_list:
#         pk=node_dict[node]
#         min_result = pd.DataFrame()
#         hour_result = pd.DataFrame()
#         for i in range(1,8):
#             dd=str((start_date + (i - 1) * unit).strftime('%Y-%m-%d'))
#             for sts in [997,998]:
#                 temp_df=uniqe_df[(uniqe_df[pk[0]].notnull())\
#                                  &(pd.to_datetime(uniqe_df[pk[0]])>=start_date+(i-1)*unit)\
#                                  &(pd.to_datetime(uniqe_df[pk[0]])<start_date+i*unit)\
#                                  &(uniqe_df[pk[2]]==sts)
#                                 ]
#                 print '%s产品%s节点%s状态为%s数据一共有数据%d条' %(product,node,dd,sts,temp_df.shape[0])
#                 if temp_df.shape[0]==0 or temp_df[pk[1]].isnull().all():
#                     continue
#                 cohort=CAS.CohortAnalysis(data=temp_df,stat_time=pk[0],end_time=pk[1])
#                 if sts==997:
#                     tmp=cohort.analysis_cohort_minute(isPercent=False)
#                     min_result=min_result.append(pd.DataFrame(data=tmp.values,index=[dd],columns=tmp.columns))
#                     # min_result.to_csv(shenpi_file_save_path+'min_result_' +product+'_'+node+'_'+(start_date+(i-1)*unit).strftime('%Y-%m-%d')+'_'+str(sts)+ '.csv',encoding='utf-8', header=True)
#                 if sts==998:
#                     tmp = cohort.analysis_cohort_hour(isPercent=False)
#                     hour_result = hour_result.append(tmp)
#                     # hour_result.to_csv(shenpi_file_save_path+'result_' +product+'_'+node+'_'+(start_date+(i-1)*unit).strftime('%Y-%m-%d')+'_'+str(sts)+ '.csv', encoding='utf-8',header=True)
#         min_result.to_csv(shenpi_file_save_path+product+'_min_result_'+node+'_997'+'.csv',encoding='utf-8', header=True)
#         hour_result.to_csv(shenpi_file_save_path +product+ '_hour_result_' + node + '_998' + '.csv', encoding='utf-8', header=True)



# 提款复提节点
# for product in products:
#     df=fliter_data(data=data,product=product)
#     draw_df=df[(df['draw_cnt']==1)&(df['draw_apprv_sts']==997)]
#     re_draw_df=df[(df['draw_cnt']==2)]
#     print '%s产品提款成功的数据%d条' %(product,draw_df.shape[0])
#     print '%s产品复提的数据%d条' % (product, re_draw_df.shape[0])
#     mer_df = pd.merge(draw_df, re_draw_df, on='user_id', suffixes=('_left', '_right'), how='left')
#     for node in redraw_node_list:
#         pk = node_dict[node]
#         min_result = pd.DataFrame()
#         hour_result = pd.DataFrame()
#         day_result =pd.DataFrame()
#         final_df=mer_df[pk]
#         if node=='redraw_appl':
#             temp_df=final_df[(final_df[pk[1]].notnull())\
#                              &(pd.to_datetime(final_df[pk[1]])>=start_date)\
#                              &(pd.to_datetime(final_df[pk[1]])<start_date+7*unit)
#                             ]
#             if temp_df.shape[0] == 0 or temp_df[pk[2]].isnull().all():
#                 continue
#             cohort = CAS.CohortAnalysis(data=temp_df, stat_time=pk[1], end_time=pk[2])
#             day_result=day_result.append(cohort.analysis_cohort_day(isPercent=False))
#             day_result.to_csv(redraw_file_save_path + product + '_day_result_' + node  + '.csv', encoding='utf-8', header=True)
#         if node=='redraw_pass':
#             for i in range(1, 8):
#                 dd=str((start_date + (i - 1) * unit).strftime('%Y-%m-%d'))
#                 for sts in [997,998]:
#                     temp_df=final_df[(final_df[pk[1]].notnull())\
#                                      &(pd.to_datetime(final_df[pk[1]])>=start_date+(i-1)*unit)\
#                                      &(pd.to_datetime(final_df[pk[1]])<start_date+i*unit)\
#                                      &(final_df[pk[3]]==sts)
#                                      ]
#                     print '%s产品%s节点%s状态为%s数据一共有数据%d条' % (product, node, dd, sts, temp_df.shape[0])
#                     if temp_df.shape[0]==0 or temp_df[pk[2]].isnull().all():
#                         continue
#                     cohort=CAS.CohortAnalysis(data=temp_df,stat_time=pk[1],end_time=pk[2])
#                     if sts==997:
#                         tmp=cohort.analysis_cohort_minute(isPercent=False)
#                         min_result=min_result.append(pd.DataFrame(data=tmp.values,index=[dd],columns=tmp.columns))
#                         # min_result.to_csv(shenpi_file_save_path+'min_result_' +product+'_'+node+'_'+(start_date+(i-1)*unit).strftime('%Y-%m-%d')+'_'+str(sts)+ '.csv',encoding='utf-8', header=True)
#                     if sts==998:
#                         tmp = cohort.analysis_cohort_hour(isPercent=False)
#                         hour_result = hour_result.append(tmp)
#                         # hour_result.to_csv(shenpi_file_save_path+'result_' +product+'_'+node+'_'+(start_date+(i-1)*unit).strftime('%Y-%m-%d')+'_'+str(sts)+ '.csv', encoding='utf-8',header=True)
#             min_result.to_csv(redraw_file_save_path+product+'_min_result_'+node+'_997'+'.csv',encoding='utf-8', header=True)
#             hour_result.to_csv(redraw_file_save_path +product+ '_hour_result_' + node + '_998' + '.csv', encoding='utf-8', header=True)







end=time.time()

print ('程序运行的时间%d'%(end-begin))






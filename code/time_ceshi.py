import datetime


t1=datetime.datetime(2019,11,18,0,0,0)
t2=datetime.datetime(2019,1,1,1,1,0)


unit=datetime.timedelta(hours=24)
for i in range(1,8):
    print i
    print t1+i*unit


# print (t2-t1).seconds
# print (t2-t1).seconds/60
# print (t2-t1).days

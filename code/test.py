import pandas as pd






df=pd.DataFrame()
data={'A':[2,2,3],'B':['wo','ni','ta']}
df1=pd.DataFrame(data)
print df1
df1.drop_duplicates(subset=['A'],keep='first',inplace=True)
print df1
df=df.append(df1)
print df
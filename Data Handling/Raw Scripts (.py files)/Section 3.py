import pandas as pd
import math

minutes = 5
filename = "eurusd_out_2018.csv"
outname = "eurusd_out_2018_5mins.csv"


df = pd.read_csv(filename,index_col= False) 


df5=df.copy()
df6=df.copy()

for i in df.index:
    n = math.floor(i/minutes) * minutes
    n2 = (n + minutes -1)
    df5.loc[i,'High'] = df.loc[n:n2,'High'].max()

for i in df.index:
    n = math.floor(i/minutes) * minutes
    n2 = (n + minutes -1)
    df6.loc[i,'Low'] = df.loc[n:n2,'Low'].min()

df5 = df5.iloc[::minutes]['High']
df6 = df6.iloc[::minutes]['Low']   

#slicing
df2 = df.iloc[::minutes]
df3 = df.iloc[(minutes-1)::minutes]['Close']
df2 = df2.drop(['High'], axis = 1)
df2 = df2.drop(['Low'], axis = 1)
df2 = df2.drop(['Close'], axis = 1)

#resetting index, so that merge can happen
df2 = df2.reset_index(drop=True)
df3 = df3.reset_index(drop=True)
df5 = df5.reset_index(drop=True)
df6 = df6.reset_index(drop=True)
df4 = pd.merge(df2, df5, left_index = True, right_index= True)
df4 = pd.merge(df4, df6, left_index = True, right_index= True)
df4 = pd.merge(df4, df3, left_index = True, right_index= True)

#rearranging
cols = df.columns.tolist()
cols = cols[:4] + [cols[-2]] + [cols[-1]]
df4 = df4[cols]

df4.index = df4['datetime']
del df4['datetime']
df4.to_csv(outname,index='datetime')


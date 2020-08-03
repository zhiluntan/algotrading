import pandas as pd
import numpy as np

#read file into pd dataframe
filename = "EURUSD_out_2017_1hr.csv"
df = pd.read_csv(filename)

#Reduce number of columns
del df['Number']
del df['Open']
del df['High']
del df['Low']

#Columns for BBands
def Strategy(DF, n):
    df = DF.copy()
    df['Mean'] = df['Close'].rolling(n).mean()
    df['BBands_Diff'] = df['Close'].rolling(n).std() * 2
    df['BBands_High'] = df['Mean'] + df['BBands_Diff']
    df['BBands_Low'] = df['Mean'] - df['BBands_Diff']
    del df['BBands_Diff']
    return df
df = Strategy(df,20)
# df['Position'] = np.where(df['Close']<df['BBands_Low'],1,0)

#To determine position, 1 means buy, then will continuously hold, -1 is sell, 
#0 is no position, 2 means close trade
df['Position1'] = 0
df['Position'] = 0

#Buy and Sell respectively
for i in df.index:
    if df.loc[i,'Close'] <= df.loc[i,'BBands_Low']:
        df.loc[i,'Position1'] = 1
    elif df.loc[i,'Close'] >= df.loc[i,'BBands_High']:
        df.loc[i,'Position1'] = -1
    elif i>=1 and df.loc[i-1,'Position1'] == 1 and \
        (df.loc[i,'Mean']-df.loc[i,'Close'])>=0.0002:
        df.loc[i,'Position1'] = 1
    elif i>=1 and df.loc[i-1,'Position1'] == -1 and \
        (df.loc[i,'Close']-df.loc[i,'Mean'])>=0.0002:
        df.loc[i,'Position1'] = -1

#Adjust so that the numbers will be there when there is a "transition" from holding to selling
for i in df.index:
    if i>=1 and df.loc[i,'Position1'] == 1 and df.loc[i-1,'Position1'] ==0:
        df.loc[i,'Position'] =1
    if i>=1 and df.loc[i,'Position1'] == -1 and df.loc[i-1,'Position1'] ==0:
        df.loc[i,'Position'] =-1
    elif i>=1 and df.loc[i,'Position1'] == 0 and df.loc[i-1,'Position1'] !=0:
        df.loc[i,'Position'] =2
df['Position'] = df['Position'].astype(np.int)
del df['Position1']


#To determine pip difference
df['Pip Diff'] = 0

#Function to find last occurrence of 1, -1 and 2. Emptylist2 to know if sell or buy.
def get_last_one(DF,n):
    emptylist = []
    emptylist2=[]
    emptylist3 = [0]
    for i in range(n):
        if DF.loc[i,'Position'] == 1:
            emptylist.append(i)
            emptylist2.append(1)
        elif DF.loc[i,'Position'] == -1:
            emptylist.append(i)
            emptylist2.append(-1)
        elif DF.loc[i,'Position'] == 2:
            emptylist3.append(i)
    return (emptylist[-1],emptylist2[-1],emptylist3[-1])

for i in df.index:
    if df.loc[i,'Position'] == 2:
        magic_index = get_last_one(df,i)[0]
        magic_buysell = get_last_one(df,i)[1]
        if magic_buysell == 1:
            df.loc[i,'Pip Diff'] = df.loc[i,'Close'] -df.loc[magic_index,'Close']
        elif magic_buysell == -1:
            df.loc[i,'Pip Diff'] = df.loc[magic_index,'Close'] -df.loc[i,'Close']

#Initial Balance
df['Position Size'] = 0
df['Profit'] = 0
df['Commission'] = 0
df['Balance'] = 100000

#Calculate cumulative balance
for i in df.index:
    if i>=1:
        df.loc[i,'Balance'] = df.loc[i-1,'Balance']
    if df.loc[i,'Position'] == 2:
        magic_index2 = get_last_one(df,i)[0]
        df.loc[i, 'Position Size'] = round(df.loc[magic_index2, 'Balance']*0.02/df.loc[magic_index2,'Close']/1000,2)
        #Profit
        df['Profit'] = df['Pip Diff'] * df['Position Size'] * 100000
#Commission
        df.loc[i,'Commission'] = df.loc[i,'Position Size']*3.76*-2

    df.loc[i,'Balance'] = df.loc[i,'Balance'] + df.loc[i,'Profit'] + df.loc[i,'Commission']
# print(df[['datetime','Position Size', 'Profit', 'Commission', 'Balance']][30:45])
# print(df[['datetime','Position Size', 'Profit', 'Commission', 'Balance']][55:58])

#Check for open positions at the end
if get_last_one(df,df.index[-1])[2] < get_last_one(df,df.index[-1])[0]:
    print("Warning: Final Position Not CLosed!")
else:
    print("All positions closed.")

asum = 0

for i in df.index:
    if df.loc[i,'Position'] == 2:
        asum += 1
        
print(asum)
# print(df['datetime'])

print("Final Balance is", round(df.loc[df.index[-1],'Balance'],2))

df.to_csv("backtestt.csv")
# print(df['Pip Diff'].sum())













# print(df['Pip Diff'].sum())
# print(type(df.loc[40,'Position']))
# a_df = df.loc[df['Position']==1]
# print(a_df.index)
# df2 = df.copy(deep=True)
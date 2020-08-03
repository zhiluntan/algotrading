import pandas as pd
from datetime import datetime

pairs = ("EURUSD", "USDCAD", "AUDUSD", "GBPUSD", "USDJPY", "USDCHF")

year = 2017
startdate = datetime(year,4,28,21)
enddate = datetime(year,4,28,22)


for i in pairs:
    filename = i + '_out.csv'
    outfile = i + '_out_2017_1hr.csv'
        
    df = pd.read_csv(filename, index_col='datetime')
    
    # changing to datetime, otherwise str wont be recognized for < & >
    df.index = pd.to_datetime(df.index)
    
    #sdf for ranging purposes, in case certain years dont start on 1st Jan etc
    sdf = (df.index>=startdate) & (df.index<=enddate)
    
    #loc by mask
    df2 = df.loc[sdf]
    
    df2.to_csv(outfile, index = 'datetime')



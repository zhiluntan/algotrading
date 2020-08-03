import pandas as pd
import datetime

pairs = ("USDCAD", "AUDUSD", "GBPUSD", "USDJPY", "USDCHF")

def dateparse(d,t):
    dt = d + " " + t
    return datetime.datetime.strptime(dt, '%Y.%m.%d %H:%M')


for i in pairs:
    filename = i + "_1_MT4.csv"
    df = pd.read_csv(filename, parse_dates={'datetime':['Date', 'Time']}, date_parser = dateparse)
    outname = i + "_out.csv"


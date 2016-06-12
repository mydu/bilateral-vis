import pandas as pd
import numpy as np

raw_data = pd.read_csv('data/trade_data.csv')

def country_list(year,raw_data = raw_data):
    """
    raw_date should be a pd.dataframe
    
    """
    trade_data_raw_year = raw_data.loc[raw_data['Yr']==year]
    country_list = set(list(trade_data_raw_year.Reporting_Entity_RIC_Name)\
                       +list(trade_data_raw_year.Partner_Entity_RIC_Name))
    country_list = sorted(list(country_list))
    return country_list

def df_year(year,raw_data = raw_data):
    return raw_data.loc[raw_data['Yr']==year]


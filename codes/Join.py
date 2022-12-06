# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 20:05:02 2022

@author: dell
"""
import pandas as pd
def join_col(df1, df2, method):
    df1 = df1.iloc[:,1:]
    df2 = df2.iloc[:,1:]
    if df1.columns[0] == df2.columns[0]:
        df = pd.merge(df1,df2)
    else:
        if method =='left':
            df = pd.merge(df1, df2, how = 'left', left_index = True, right_index = True)
        if method == 'right':
            df = pd.merge(df1, df2, how = 'right', left_index = True, right_index = True )
        if method == 'inner':
            df = pd.merge(df1, df2, how = 'inner', left_index = True, right_index = True)
        if method == 'outer':
            df = pd.merge(df1, df2, how = 'outer', left_index = True, right_index = True)
    return df    
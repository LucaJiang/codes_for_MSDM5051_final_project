# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 20:44:09 2022

@author: dell
"""
#%%
import numpy as np
import pandas as pd
# colnames = ['1', '2', '3', '4', '5', '6', '7', '8']
# TDCS = pd.read_csv('C:\\Users\\dell\\Desktop\\TDCS_M06A.csv', names=colnames, header=None)

import time

#%%
# called by count_sort
def insert_sort(array):
    # copy from sample code
    n = len(array)
    if n <= 1:
        return array
    for i in range(1, n):  # The new card: (1, 2, ..., n-1)
        for j in range(i, 0, -1):  # From the new card to old cards
            if array[j] < array[j - 1]:
                array[j], array[j - 1] = array[j - 1], array[j]
            else:
                break
    return array
 
    
# combine count_sort and insert_sort
def _count_sort_df(df, col, order):
    n = len(df)
    type_dict = {}
    for i in range(n):
        key = df.loc[:,col][i]
        type_dict.setdefault(key, []).append(i)
    key_sort = insert_sort(list(type_dict.keys()))
    i = 0
    index_order = []
    for key in key_sort:
        index_order += type_dict[key]
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]

#%%
def _partition1(index_order, ele, left, right):
    # partition: Hoare partition scheme
    #! really be careful the repeat valuessss!

    p = right - 1
    right -= 2
    while left <= right:  # must include =, e.g. r=l=0 p=1 ap<ar
        while left <= right and ele[left] <= ele[p]:
            left += 1
        while left <= right and ele[right] > ele[p]:
            # second judgement not include =, in case out of range
            # when l==r already
            right -= 1
        if left < right:
            ele[left], ele[right] = ele[right], ele[left]
            index_order[left], index_order[right] = index_order[right], index_order[left]
        
    # left >= right
    ele[left], ele[p] = ele[p], ele[left]
    index_order[left], index_order[p] = index_order[p], index_order[left]
    #print(index_order)
    return left


def _quick_sort1(index_order, ele, low, high):
    # low=0, high=len, [low, high)
    if high - low <= 1:
        return index_order
    p = _partition1(index_order, ele, low, high)
    _quick_sort1(index_order, ele, low, p)
    _quick_sort1(index_order, ele, p, high)
    return index_order


# conbine quick_sort and partition
def _quick_sort_df(df, col, order):
    # low=0, high=len, [low, high)
    n = len(df)
    df_copy = df.copy()
    index_order =  np.linspace(0,n-1,n)
    ele = df_copy.loc[:,col].to_numpy() 
    
    index_order = _quick_sort1(index_order, ele, 0, n)
    
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]

#%%
def _count_sort1(index_order, ele):
    n = len(index_order)
    type_dict = {}
    for i in range(n):
        key = ele[i]
        type_dict.setdefault(key, []).append(index_order[i])
    key_sort = insert_sort(list(type_dict.keys()))
    i = 0
    index_order = []
    for key in key_sort:
        index_order += type_dict[key]
    return index_order


# sort time
# conbine quick_sort and partition and count_sort
def _quick_sort_stack_df(df, col, order, small_set_sort_func=_count_sort1, threshold=256):
    
    n = len(df)
    df_copy = df.copy()
    index_order =  np.linspace(0,n-1,n)
    ele = df_copy.loc[:,col].to_numpy() 
    
    if col == 'DerectionTime_O' or col =='DerectionTime_D':
        timeconvrt = lambda x: x[9:11]+x[12:14]
        ele = [timeconvrt(i) for i in ele]
        
    stack = [[-1, -1]] * (n // 2)
    stack[0] = [0, n]
    num = 1
    while num:
        num -= 1
        [i, j] = stack[num]
        p = _partition1(index_order, ele, i, j)
        
        if j - p > threshold:
            stack[num] = [p, j]
            num += 1
        else:
            index_order[p:j] = small_set_sort_func(index_order[p:j], ele[p:j])
        if p - i > threshold:
            stack[num] = [i, p]
            num += 1
        else:
            index_order[i:p] = small_set_sort_func(index_order[i:p], ele[i:p])
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]


#%%
def ordered_merge1(ele1, index_order1, ele2, index_order2):
    cnt1, cnt2 = 0, 0
    ele = []
    index_order = []
    while cnt1 < len(ele1) and cnt2 < len(ele2):
        if ele1[cnt1] < ele2[cnt2]:
            ele.append(ele1[cnt1])
            index_order.append(index_order1[cnt1])
            cnt1 += 1
        else:
            ele.append(ele2[cnt2])
            index_order.append(index_order2[cnt2])
            cnt2 += 1
            
    ele += ele1[cnt1 :]
    ele += ele2[cnt2 :]    
    index_order += index_order1[cnt1 :]
    index_order += index_order2[cnt2 :]
    return index_order,ele


def _merge_sort1(index_order, ele):
    if len(ele) <= 1:
        return index_order, ele
    mid = (len(ele) + 1) // 2
    idx1, sub1 = _merge_sort1(index_order[: mid], ele[: mid])
    idx2, sub2 = _merge_sort1(index_order[mid :], ele[mid :])
    return ordered_merge1(sub1, idx1, sub2, idx2)
    
    
def _merge_sort_df(df, col, order):   
    n = len(df)
    df_copy = df.copy()
    index_order =  list(np.linspace(0,n-1,n))
    ele = df_copy.loc[:,col].tolist() 
    
    index_order, ele = _merge_sort1(index_order, ele)
    
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]


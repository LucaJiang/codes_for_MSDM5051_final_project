# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 02:01:06 2022

@author: dell
"""
import numpy as np

class Heap():
    def __init__(self, array1, array2):
        self.heap = array1
        self.index = array2
        self.length = len(array1)
        self.build_max_heap()
    
    def left(self, idx):
        pos = 2 * idx + 1
        return pos if pos < self.length else None

    def right(self, idx):
        pos = 2 * idx + 2
        return pos if pos < self.length else None

    def parent(self, idx):
        return (idx - 1) // 2 if idx > 0 else None

    def build_max_heap(self):
        last_to_heapify = self.parent(self.length - 1)
        # lower limit of loop is 0
        for i in range(last_to_heapify, -1, -1): 
            self.max_heapify(i)
    
    def _greater_child(self, i):
        left, right = self.left(i), self.right(i)
        if left is None and right is None:
            return None
        elif left is None:
            return right
        elif right is None:
            return left
        else:
            return left if self.heap[left]>self.heap[right] else right

    def max_heapify(self, i):
        greater_child = self._greater_child(i)
        if greater_child is not None and self.heap[greater_child] > self.heap[i]:
            self.heap[i], self.heap[greater_child] = self.heap[greater_child], self.heap[i]
            self.index[i], self.index[greater_child] = self.index[greater_child], self.index[i]
            self.max_heapify(greater_child)

    def sort(self):
        while self.length > 1:
            self.heap[0], self.heap[self.length - 1] = self.heap[self.length - 1], self.heap[0]
            self.index[0], self.index[self.length - 1] = self.index[self.length - 1], self.index[0]
            self.length -= 1
            self.max_heapify(0)
        return self.heap, self.index


def _heap_sort(array1, array2):
    my_heap = Heap(array1, array2)
    return my_heap.sort()


def _heap_sort_df(df, col, order):
    n = len(df)
    df_copy = df.copy()
    index_order =  np.linspace(0,n-1,n)
    ele = df_copy.loc[:,col].to_numpy() 
    
    ele, index_order = _heap_sort(ele, index_order)
    
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 01:09:47 2022

@author: dell
"""
import numpy as np

import binary_tree1

class Node(binary_tree1.Node):
    def left_height(self):
        return -1 if self.left is None else self.left.height
    def right_height(self):
        return -1 if self.right is None else self.right.height
    def update_height(self):
        self.height = max(self.left_height(), self.right_height()) + 1
    def balance(self):
        "-2, -1: left heavy, 1, 2: right heavy"
        return self.right_height() - self.left_height()

class BinarySearchTree(binary_tree1.BinaryTree):
    def __init__(self, data_array = [], index_order = []):
        self.root = None
        for i in range(len(data_array)):
            self.insert(Node(data_array[i], index_order[i]))

    
    def insert(self, new_node, node = 0):
        if not self.root:
            self.root = new_node
            return new_node
        if node == 0:
            node = self.root
        if new_node.data < node.data:
            if node.left:
                self.insert(new_node, node.left)
            else:
                new_node.parent = node
                node.left = new_node
        else:
            if node.right:
                self.insert(new_node, node.right)
            else:
                new_node.parent = node
                node.right = new_node
        node.update_height()

    def sort(self):
        return self.inorder()

def BST_sort(array1, array2):
    my_tree = BinarySearchTree(array1, array2)
    return my_tree.sort()

def BST_sort_df(df, col, order):
    n = len(df)
    df_copy = df.copy()
    index_order =  np.linspace(0,n-1,n)
    ele = df_copy.loc[:,col].to_numpy() 
    
    ele, index_order = BST_sort(ele, index_order)
    
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]
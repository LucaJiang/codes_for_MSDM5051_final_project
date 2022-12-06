# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 01:22:57 2022

@author: dell
"""
import numpy as np

import binary_search_tree1

class Node(binary_search_tree1.Node):
    pass

class AVLTree(binary_search_tree1.BinarySearchTree):
    def insert(self, new_node, node = 0):
        super().insert(new_node, node)
        self.check_fix_AVL(new_node.parent)
        return new_node
    
    def update_all_heights_upwards(self, node):
        node.update_height()
        if node is not self.root:
            self.update_all_heights_upwards(node.parent)
    
    def _left_rotate(self, x): 
        # x, y, B notation follows MIT 6.006 Lecture 6.
        # First define y and B:
        y = x.right
        B = y.left
        # Setup y:
        y.parent = x.parent
        y.left = x
        # Setup y's parent
        if y.parent is None:
            self.root = y
        elif y.parent.left is x:
            y.parent.left = y
        else:
            y.parent.right = y
        # Setup x:
        x.parent = y
        x.right = B
        # Setup B:
        if B is not None:
            B.parent = x
        self.update_all_heights_upwards(x)

    def _right_rotate(self,x):
        # First define y and B:
        y = x.left
        B = y.right
        # Setup y:
        y.parent = x.parent
        y.right = x
        # Setup y's parent
        if y.parent is None:
            self.root = y
        elif y.parent.right is x:
            y.parent.right = y
        else:
            y.parent.left = y
        # Setup x:
        x.parent = y
        x.left = B
        # Setup B:
        if B is not None:
            B.parent = x
        self.update_all_heights_upwards(x)

    def check_fix_AVL(self, node):
        if node is None:
            return
        if abs(node.balance()) < 2:
            self.check_fix_AVL(node.parent)
            return
        if node.balance() == 2: # right too heavy
            if node.right.balance() >= 0:
                self._left_rotate(node)
            else:
                self._right_rotate(node.right)
                self._left_rotate(node)
        else: # node.balance() == -2, left too heavy
            if node.left.balance() <= 0:
                self._right_rotate(node)
            else:
                self._left_rotate(node.left)
                self._right_rotate(node)
        self.check_fix_AVL(node.parent)

def AVL_sort(array1, array2):
    my_tree = AVLTree(array1, array2)
    return my_tree.sort()

def AVL_sort_df(df, col, order):
    n = len(df)
    df_copy = df.copy()
    index_order =  np.linspace(0,n-1,n)
    ele = df_copy.loc[:,col].to_numpy() 
    
    ele, index_order = AVL_sort(ele, index_order)
    
    if order == 1:
        return index_order
    if order == -1:
        return index_order[::-1]


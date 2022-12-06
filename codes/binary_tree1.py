# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 00:14:56 2022

@author: dell
"""
class Node:
    def __init__(self, data, index):
        self.left = None
        self.right = None
        self.parent = None
        self.data = data
        self.index = index
        self.height = 0

class BinaryTree:

    def __init__(self):
        self.root = None

    # def __str__(self, node = 0, depth = 0, direction_label = ""):
    #     "The tree structure in string form, to be used in str(my_node) or print(my_node)."
    #     if node == 0:
    #         node = self.root
    #     if node:
    #         height_info = "(H"+str(node.height)+")" if node.height > 0 else ""
    #         return depth * "\t" + direction_label + height_info + str(node.data) + "\n" + \
    #             self.__str__(node.left, depth+1, "L:") + self.__str__(node.right, depth+1, "R:")
    #     else:
    #         return ""

    def inorder(self, node = 0, result = None, index_order = None):
        if result is None:
            result = []
        if index_order is None:
            index_order = []
        if node == 0:
            node = self.root
        if node:
            self.inorder(node.left, result, index_order)
            result.append(node.data)
            index_order.append(node.index)
            self.inorder(node.right, result, index_order)
        return result, index_order

    



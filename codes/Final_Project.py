# -*- coding: utf-8 -*-
"""
Created on Dec  4  20:32:29 2022

@author: DAI Yuxin
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd
from tkinter import ttk
from tkinter import INSERT
from bplustree import BPlusTree
#import heap1
from search import Search, Search_from_to
from heap1 import _heap_sort_df as Heap_sort
from sort1 import _quick_sort_df as Quick_sort
from sort1 import _count_sort_df as Counting_sort
from sort1 import _quick_sort_stack_df as Quick_stack_sort
from sort1 import _merge_sort_df as Merge_sort
from binary_search_tree1 import BST_sort_df as BST_sort
from AVL_tree1 import AVL_sort_df as AVL_sort
from Join import join_col


class dataset(object):

    def __init__(self):
        self.df = pd.DataFrame(data=[])
        self.search_column = ''
        self.search_value = ''
        self.sort_column = ''
        self.sort_algorithm = ''
        self.sort_order = 1

    def import_csv_data(self):
        global v
        textup.insert(INSERT, 'Data import...\n')
        csv_file_path = askopenfilename()
        v.set(csv_file_path)
        self.df = pd.read_csv(csv_file_path, header=None)
        self.df.columns = [
            'VehicleType', 'DerectionTime_O', 'GantryID_O', 'DerectionTime_D',
            'GantryID_D', 'TripLength', 'TripEnd', 'TripInformation'
        ]
        self.df.drop('TripInformation', axis=1, inplace=True)
        textup.insert(INSERT, self.df)
        textup.insert(INSERT, '\n')

    def export_csv_data(self):
        column = importbox.get()
        if column == 'All':
            dfnew = self.df
        else:
            dfnew = self.df[column]
        dfnew.to_csv('newpart.csv')
        textup.insert(INSERT, '\nSaved\n')

    def search(self):
        self.search_column = searchbox.get()
        self.search_value = searchentry.get()
        textup.insert(INSERT, 'Search colunmn: ' + self.search_column)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Search value: ' + self.search_value)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Search...\n')
        vlist = self.df[self.search_column]
        print(vlist)
        # build tree
        bplustree = BPlusTree(order=4)
        print('aim:')
        print(self.search_value)
        for i in range(self.df.shape[0]):
            bplustree.insert(vlist[i], i)
        results = Search(aim=self.search_value, tree=bplustree)
        print('results:')
        textup.insert(INSERT, 'results:\n')
        self.df = self.df.take(results)
        textup.insert(INSERT, self.df)

    def sort(self):

        self.sort_column = sortbox.get()
        self.sort_algorithm = albox.get()
        order = orderbox.get()
        percent = percentbox.get()
        p = float(percent.strip('%')) / 100
        if order == 'Ascending order':
            self.sort_order = 1
        else:
            self.sort_order = -1
        textup.insert(INSERT, 'Sort colunmn: ' + self.sort_column)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Sort algorithm: ' + self.sort_algorithm)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Sort...\n')
        results = eval(self.sort_algorithm)(self.df, self.sort_column,
                                            self.sort_order)
        lenth = self.df.shape[0]
        range_sort = int(p * lenth)
        print(range_sort)
        textup.insert(INSERT, 'results:\n')
        self.df = self.df.take(results[:range_sort])
        textup.insert(INSERT, self.df)

    def search_from_to(self):
        self.search_column = frombox.get()
        #self.search_value = searchentry.get()
        _from = _fromentry.get()
        _to = _toentry.get()
        textup.insert(INSERT, 'Search colunmn: ' + self.search_column)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Search from: ' + _from)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Search to: ' + _to)
        textup.insert(INSERT, '\n')
        textup.insert(INSERT, 'Search...\n')
        vlist = self.df[self.search_column]
        print(vlist)
        # build tree
        bplustree = BPlusTree(order=4)
        print('aim:')
        print(self.search_value)
        for i in range(self.df.shape[0]):
            bplustree.insert(vlist[i], i)
        results = Search_from_to(bplustree, _from, _to)
        print('results:')
        textup.insert(INSERT, 'results:\n')
        self.df = self.df.take(results)
        textup.insert(INSERT, self.df)


def start():
    data.import_csv_data()


def join_df():
    global v1, v2
    textup.insert(INSERT, 'Join...\n')
    method = joinbox.get()
    csv_file_path1 = askopenfilename()
    v1.set(csv_file_path1)
    csv_file_path2 = askopenfilename()
    v2.set(csv_file_path2)
    df1 = pd.read_csv(csv_file_path1)
    df2 = pd.read_csv(csv_file_path2)
    data.df = join_col(df1, df2, method)
    textup.insert(INSERT, data.df)


global data
global df1, df2
data = dataset()
root = tk.Tk()
w, h = root.maxsize()
root.geometry("{}x{}".format(w, h))
root.title('Inquiry system for Taiwan traffic data')

Title = tk.Label(root,
                 text='Inquiry System for Taiwan Traffic Data',
                 fg='black',
                 font=('Times', 20))
Title.grid(row=0, column=0, rowspan=2, columnspan=5)
Name = tk.Label(root,
                text='Designed by DAI Yuxin, JIANG Wenxin, WANG Ziyu',
                fg='black',
                pady=20,
                font=('Times', 12))
Name.grid(row=2, column=0, columnspan=5)

datainfo = tk.Message(
    root,
    text=
    'Data description: https://web.archive.org/web/20191103004550/http://tisvcloud.freeway.gov.tw/TISVCloud_web.files/TDCS_M06A.htm',
    fg='black',
    width=800,
    pady=50,
    font=('Times', 12))
datainfo.grid(row=3, column=0, sticky='nw', columnspan=3)
v = tk.StringVar()

textup = tk.Text(root, width=100, height=25, undo=True, autoseparators=True)
textup.grid(row=3, column=3, sticky='e')
textup.insert('insert', 'start\n')

tk.Button(root, text='Import Data', command=start).grid(row=3, column=0)
tk.Button(root, text='Clear', command=textup.edit_undo).grid(row=4,
                                                             column=3,
                                                             sticky='ne')
tk.Button(root, text='Export Data',
          command=data.export_csv_data).grid(row=3, column=1, sticky='e')

importbox = ttk.Combobox(root)
importbox.grid(row=3, column=2)
importbox['value'] = ('All', 'VehicleType', 'DerectionTime_O', 'GantryID_O',
                      'DerectionTime_D', 'GantryID_D', 'TripLength')
importbox.current(0)

tk.Button(root, text='Search', command=data.search).grid(row=5,
                                                         column=0,
                                                         sticky='n')
tk.Button(root, text='Sort', command=data.sort).grid(row=4,
                                                     column=0,
                                                     padx=50,
                                                     pady=20)

searchbox = ttk.Combobox(root)
searchbox.grid(row=5, column=1, stick='n')
searchbox['value'] = ('VehicleType', 'DerectionTime_O', 'GantryID_O',
                      'DerectionTime_D', 'GantryID_D')
searchbox.current(0)
tk.Label(root, text='Search value:').grid(row=5, column=2, stick='n')
searchentry = tk.Entry(root)
searchentry.grid(row=5, column=3, stick='nw')

sortbox = ttk.Combobox(root)
sortbox.grid(row=4, column=1)
sortbox['value'] = ('VehicleType', 'DerectionTime_O', 'GantryID_O',
                    'DerectionTime_D', 'GantryID_D', 'TripLength')
sortbox.current(0)

albox = ttk.Combobox(root)
albox.grid(row=4, column=2)
albox['value'] = ('Counting_sort', 'Heap_sort', 'AVL_sort', 'Merge_sort',
                  'Quick_stack_sort')
albox.current(0)

orderbox = ttk.Combobox(root)
orderbox.grid(row=4, column=3, sticky='w')
orderbox['value'] = ('Ascending order', 'Descending order')
orderbox.current(0)

percentbox = ttk.Combobox(root)
percentbox.grid(row=4, column=3)
percentbox['value'] = ('20%', '50%', '80%', '100%')
percentbox.current(0)

tk.Button(root, text='Join', command=join_df).grid(row=7, column=0)
joinbox = ttk.Combobox(root)
joinbox.grid(row=7, column=1)
joinbox['value'] = ('left', 'right', 'inner', 'outer')
joinbox.current(0)

tk.Button(root, text='Search from_to',
          command=data.search_from_to).grid(row=6,
                                            column=0,
                                            stick='s',
                                            pady=20)
frombox = ttk.Combobox(root)
frombox.grid(row=6, column=1)
frombox['value'] = ('DerectionTime_O', 'DerectionTime_D', 'TripLength')
joinbox.current(0)
_fromentry = tk.Entry(root)
_fromentry.grid(row=6, column=2)
_toentry = tk.Entry(root)
_toentry.grid(row=6, column=3, stick='w')

v1 = tk.StringVar()
v2 = tk.StringVar()
tk.Label(root, text='File Path1:').grid(row=7, column=2)
tk.Label(root, text='File Path2:').grid(row=8, column=2)
entry1 = tk.Entry(root, textvariable=v1, width=40).grid(row=7,
                                                        column=3,
                                                        stick='w')
entry2 = tk.Entry(root, textvariable=v2, width=40).grid(row=8,
                                                        column=3,
                                                        stick='w')


def usr_log_in():

    def log_in():
        window_sign_up.wm_attributes('-topmost', False)
        tk.messagebox.showinfo('Welcome!', 'You have successfully logged in!')
        window_sign_up.destroy()

    window_sign_up = tk.Toplevel(root)
    window_sign_up.geometry('400x200')
    window_sign_up.attributes("-toolwindow", 1)

    window_sign_up.title('Log in window')
    window_sign_up.wm_attributes('-topmost', 1)

    new_name = tk.StringVar()
    new_name.set('MSDM5051 user')
    tk.Label(window_sign_up, text='User name: ').grid(column=0, row=0)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.grid(column=1, row=0)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').grid(column=0, row=1)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.grid(column=1, row=1)

    btn_comfirm_sign_up = tk.Button(window_sign_up,
                                    text='Log in',
                                    command=log_in)
    btn_comfirm_sign_up.grid(column=1, row=2)


usr_log_in()

root.mainloop()
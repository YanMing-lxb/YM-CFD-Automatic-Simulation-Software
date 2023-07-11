'''
 =======================================================================
 ····Y88b···d88P················888b·····d888·d8b·······················
 ·····Y88b·d88P·················8888b···d8888·Y8P·······················
 ······Y88o88P··················88888b·d88888···························
 ·······Y888P··8888b···88888b···888Y88888P888·888·88888b·····d88b·······
 ········888······"88b·888·"88b·888·Y888P·888·888·888·"88b·d88P"88b·····
 ········888···d888888·888··888·888··Y8P··888·888·888··888·888··888·····
 ········888··888··888·888··888·888···"···888·888·888··888·Y88b·888·····
 ········888··"Y888888·888··888·888·······888·888·888··888··"Y88888·····
 ·······························································888·····
 ··························································Y8b·d88P·····
 ···························································"Y88P"······
 =======================================================================

 -----------------------------------------------------------------------
Author       : 焱铭
Date         : 2023-07-11 12:54:06 +0800
LastEditTime : 2023-07-11 20:46:33 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : \CFD-Automatic-Simulation-Software\Functional_modules\Prepare.py
Description  : 
 -----------------------------------------------------------------------
'''

import os
import csv
import xlrd
import numpy as np
import PySimpleGUI as sg

#  准备工作
class Prepare(object):
    def __init__(self, window, path, scripts_output_path, result_output_path):  # path：实验规划表所在路径
        self.window =window
        self.path = path
        self.scripts_path = scripts_output_path
        self.result_path = result_output_path
        self.Response_Name = []  # 响应名称

    #  读取实验规划表
    def excel(self, G_num, W_num, Reslut_num):  # G_num：几何参数数量，W_num:物理参数数量

        index_all=[]
        G_name = []
        W_name =[]
        self.Response_Name.clear()

        # 读取正交规划表
        workbook = xlrd.open_workbook(self.path)  # 括号中为文件路径
        # 打开excel数据表
        table = workbook.sheet_by_index(0)  # 通过索引读取
        for i in range(2, table.nrows):  # table.nrows 表示最后一行
            index = int(table.cell(i, 0).value)
            index_all.append(index)

        excel_Gdata = np.zeros([len(index_all), G_num])
        excel_Wdata = np.zeros([len(index_all), W_num])

        for i in range(2, table.nrows):  # table.nrows 表示最后一行
            for j in range(G_num):
                excel_Gdata[i-2][j] = float(table.cell(i, j + 1).value)
            for j in range(W_num):
                excel_Wdata[i-2][j] = float(table.cell(i, j + G_num + 1).value)

        for j in range(G_num):
            G_name.append(table.cell(1, j + 1).value)
        for j in range(W_num):
            W_name.append(str(table.cell(1, j + G_num + 1).value))

        RRS_Gdata = np.array(list(set([tuple(t) for t in excel_Gdata]))).tolist() # numpy数组去重，然后转换为数组
        for i in range(len(RRS_Gdata)): # 将浮点形数组转换为字符型
            for j in range(G_num):
                RRS_Gdata[i][j]=str(RRS_Gdata[i][j])

        excel_Wdata = excel_Wdata.tolist()
        excel_Gdata = excel_Gdata.tolist()
        for i in range(len(index_all)):
            for j in range(G_num):
                excel_Gdata[i][j]=str(excel_Gdata[i][j])
            for j in range(W_num):
                excel_Wdata[i][j] = str(excel_Wdata[i][j])

        for j in range(Reslut_num):
            self.Response_Name.append(table.cell(1, j + W_num + G_num+1).value)

        self.window['state_print'].print("********** 已从实验规划中读取数据 **********", text_color='red')
        self.window['state_print'].print(" ")

        return index_all, G_name, W_name, excel_Gdata, excel_Wdata, RRS_Gdata, 


    #  创建result.csv文件
    def create_csv(self):  # 结果文件所在文件夹路径
        if os.path.exists(os.path.dirname(self.path) + '/Result.csv'):
            os.remove(os.path.dirname(self.path) + '/Result.csv')
        with open(os.path.dirname(self.path) + '/Result.csv', 'w') as f:
            csv_write = csv.writer(f)
            csv_head = self.Response_Name
            csv_write.writerows([csv_head])

    #  创建文件夹
    def create_folder(self):
        if not os.path.exists(self.scripts_path):
            os.makedirs(self.scripts_path)
            self.window['state_print'].print("*****脚本文件夹已经创建*****", text_color='red')
            sg.cprint("*****脚本文件夹已经创建*****", text_color='red')
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
            self.window['state_print'].print("*****结果文件夹已经创建*****", text_color='red')
            sg.cprint("*****结果文件夹已经创建*****", text_color='red')
        else:
            self.window['state_print'].print("*****文件夹已经存在了*****", text_color='red')
            sg.cprint("*****已存在脚本文件夹、结果文件夹，无需创建*****", text_color='red')
        self.window['state_print'].print(" ")
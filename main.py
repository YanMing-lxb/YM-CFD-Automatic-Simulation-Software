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

Author       : 焱铭
Date         : 2022-08-25 19:20:39 +0800
LastEditTime : 2023-07-05 16:38:25 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : \CFD-Automatic-Simulation-Software\main.py
Description  : 
------------------------------------------------------------------------
'''
import sys
import csv
import os
import re
import time
import xlrd
import xlwt
import pyautogui
import threading
import subprocess
import numpy as np
from os import walk
from os.path import join
import PySimpleGUI as sg
from xlutils.copy import copy
from PIL import Image
import base64
from io import BytesIO



manual = "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000使用说明书\n\n" \
        "\000\000\000\000本程序原理是依照实验规划表对fluent_meshing、fluent、CFD_Post脚本进行修改，并依次运行脚本以达到自动仿真的作用，因此在使用本程序之前需注意以下几点：\n\n"\
        "1.\0定义：\n"\
        "\000\000\000a.\0几何变量：改变几何的变量\n"\
        "\000\000\000b.\0物理变量：其他改变物理参数的变量，如流速、温度、材料参数等；物理变量为直" \
        "\000\000\000\000\000\000\000接输入脚本中的数据，如有类似纳米流体体积分数这种需要换算成特定体积分数的" \
        "\000\000\000\000\000\000\000纳米流体物性参数的，如将体积分数换算成密度、比热容、导热率、粘度的，则物" \
        "\000\000\000\000\000\000\000理变量数目按照换算后的个数来计算，即体积分数占4个物理变量。\n"\
        "\000\000\000c.\0响应数目：应得到的响应的数目\n"\
        "\000\000\000d.\0环境温度：初始化时所有部件的温度\n\n"\
        "\000\000\000准。\n\n"\
        "2.\0实验规划表为excel文件，需放在.xls后缀的excel文件中，注意第一列为序号、几何变" \
        "\000\000\000量需放在前几列、后面为物理变量、最后为响应值；\n\n"\
        "3.\0使用本软件之前需制作脚本模板。本程序修改模板原理是寻找关键词，替换为实验规划" \
        "\000\000\000表中对应变量，因此脚本模板中除几个特殊的关键词其他关键词需与实验规划表中变量" \
        "\000\000\000名称一致。\n\n"\
        "4.\0特殊关键词：如inlet温度与环境温度相同，可以将inlet温度替换为关键字：环境温度\n"\
        "\000\000\000a.\0fluent中：输入、输出、温度单位、迭代次数、环境温度\n"\
        "\000\000\000b.\0fluent_meshing中：输入、输出\n"\
        "\000\000\000c.\0cfd_post中：输入、输出、温度单位、序号、结果文件路径\n\n"\
        "5.\0模板脚本名称为固定名称分别为：fluent.txt（utf-8）、fluent_meshing.txt（utf-8" \
        "\000\000\000）、cfd_post.cse（ansi）（可以文本文档打开编辑）。其中cfd_post.cse文件为cfd_" \
        "\000\000\000post生成的文件否则会出现编码错误\n\n"\
        "6.\0几何模型无法自动生成，因此需要DM导出的几何模型其后缀为.agdb。\n\n"\
        "7.\0文件命名规则：\n"\
        "\000\000\000a.\0几何模型：Geom-几何变量1-几何变量2.agdb,依次往下类推,几何变量3等（如，有" \
        "\000\000\000\000\000\000几何变量；布局：1、2、3，当量直径：0.5、0.8、1、特征长度：7、14、21此时几" \
        "\000\000\000\000\000\000何模型命名应为：Geom-1-0.5-14.agdb）\n"\
        "\000\000\000b.\0网格文件：命名规则与几何模型相同，Mesh-几何变量1-几何变量2.msh依次往下类" \
        "\000\000\000\000\000\000推几何变量3等\n"\
        "\000\000\000c.\0fluent结果文件自动生成，无需注意。\n\n\n\n\n\n\n\n\n\n"\
        ""

scripts_path = os.path.dirname(sys.argv[0]) + "\ANSYS_Python_Project\Script"  # 生成的脚本文件路径
result_path = os.path.dirname(sys.argv[0]) + "\ANSYS_Python_Project\Result"  # 网格文件路径，几何文件路径，结果文件路径

index_all = []      # 实验序号 数组
G_name = []         # 几何变量名称 数组
W_name = []         # 物理变量名称 数组

content_beach = """iVBORw0KGgoAAAANSUhEUgAAABgAAAAPCAYAAAD+pA/bAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAABmSURBVDhP1ZRBCsAgDATTnvOoPD0/a9kggqQKxezBuYhs2AEDXqr6CJG7nTRC4O5xmbGTh8DMlkM7eX8ilmTYAUOSllwtSQJQKfkUIMTQjD95ElSWg0FQXQ66gFEOQsAqB6d/diIv1qNjI1hTIysAAAAASUVORK5CYII="""
content_save = """iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAHcSURBVDhPrVTNK0RRFD8j/4CVrCRZaGxYKo2FBYqoKQuFhWg2iAUrayVZKrGYWSgfpbCRka+yYCHlOytWdrOf+95zfufc613TsOHUfefjnvs7v3PunUkUCoWI/kEEaHnjhcIooqIJyQSh6KKJxDZWS6zEN4Ge2VtKUSXQANJcXUOXb++0OBlyBCRZJ6z+WrHfkYmos76Bdh8e2ScFAmpo0ZF8MZ6j0BiKeIXFoi7P7zqckNzd8zUyVa2AUCBQDUIAacW21UHR8fKZqa1tB7a4xyhgRthEO6dD62WZwMbqOZuW+fS0jtLW3b0PFDEQM7OM2nPDossxcbaMQ7qA77WGoDDixHx6pSwTF+u7mpVcKc7MIArETGJ0vpGdMdGu+jc7ofaPjDCjVG0d9c+8io8E907g+zZ0ujEZz5VFHmRm4VpAUAHPAAm4RVBHTHxeansx1tmbW3re7rXDZlQHsv/08isT5w8km7y358+Ig0qVNz8uOMaH5J0YsfOb8zwiHWzLyJHN17FAKvCB46hK1RIQaAeCL4oBJH7EFgiH3UyknRIQ+BA5Yn/cmh8P296agmBOsA+yc7LpDvo2tOtA8hkU8vV/1D11IiDSGieqjv3ve8oEIDhcOB6Igf4mRJ/SoWmfLfO/ggAAAABJRU5ErkJggg=="""
content_yes = """iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAEjSURBVDhPrZThsYIwEISjw//XhB1gB68IOrAEi6AD7cAi6EA7sAx+MuPLbm7DkYDvh26G4ZJcPpZwYTeO4yt8QQRN02TdWbefp0WP2Hij+kOXAqemaWrQDEgyTAxyFNrYPLACAYIkCMvYIqAShmLacOjZXYA85BqbAB6k+aRHaFs46wna22iWILq84PB+ujBi380TpH3Rq5QA6XW6845ZXefnGUNLRwBtSZBSeqaB6CW7KRf5/u56tCiKkEQiaM2HFm9CCiVHIK3sy1tIkZ73SOP4xOWid05UEgStlb0Wr0Kcm75LRZkdkWwJKrv/IChIaXFEflETtlcuP6kYAGPoBsZVZePs+KdQAFSQNkOkzd8IKjaZmyl4fe2JVz601v9AIfwBWyytn1UYFGIAAAAASUVORK5CYII="""

beach_image=Image.open(BytesIO(base64.b64decode(content_beach.encode("utf8"))))
save_image=Image.open(BytesIO(base64.b64decode(content_save.encode("utf8"))))
yes_image=Image.open(BytesIO(base64.b64decode(content_yes.encode("utf8"))))


# ----------------------------------------------------------------------
    # 打包后资源文件目录访问
# ----------------------------------------------------------------------   
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('')
os.chdir(cd)



#  搜索并删除文件
def SearchFile_remove(path, suffix, key_word):
    for root, dirs, files, in walk(path):
        for i in files:
            if os.path.isfile(path + '/' + i):
                if i.endswith(suffix):
                    if key_word == "任意":
                        os.remove(join(root, i))
                        window['state_print'].print('已删除：' + i + ' 文件', text_color='blue')
                    if key_word in i:
                        os.remove(join(root, i))
                        window['state_print'].print('已删除：' + i + ' 文件', text_color='blue')


#  进度条
def progress(name, all_num, num):
    window['进度名称'].update(value=name + '：')
    window['进度'].update(value="▋" * int(num / all_num * 100 / 1.4))
    window['百分比'].update(value="{}%".format(int(num / all_num * 100)))


#  准备工作
class Prepare(object):
    def __init__(self, path, scripts_output_path, result_output_path):  # path：实验规划表所在路径
        self.path = path
        self.scripts_path = scripts_output_path
        self.result_path = result_output_path
        self.Response_Name = []  # 响应名称

    #  读取实验规划表
    def excel(self, G_num, W_num, Reslut_num):  # G_num：几何参数数量，W_num:物理参数数量

        index_all.clear()
        G_name.clear()
        W_name.clear()
        global excel_Gdata
        global excel_Wdata
        global RRS_Gdata
        self.Response_Name.clear()

        # 读取正交规划表
        workbook = xlrd.open_workbook(self.path)  # 括号中为文件路径
        # 打开excel数据表
        table = workbook.sheet_by_index(0)  # 通过索引读取
        for i in range(2, table.nrows):  # table.nrows 表示最后一行
            index = int(table.cell(i, 0).value)
            index_all.append(index)

        excel_Gdata = np.zeros([len(index_all), G_num])
        excel_Wdata = np.zeros([len(index_all),W_num])

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

        window['state_print'].print("********** 已从实验规划中读取数据 **********", text_color='red')
        window['state_print'].print(" ")


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
            window['state_print'].print("*****脚本文件夹已经创建*****", text_color='red')
            sg.cprint("*****脚本文件夹已经创建*****", text_color='red')
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
            window['state_print'].print("*****结果文件夹已经创建*****", text_color='red')
            sg.cprint("*****结果文件夹已经创建*****", text_color='red')
        else:
            window['state_print'].print("*****文件夹已经存在了*****", text_color='red')
            sg.cprint("*****已存在脚本文件夹、结果文件夹，无需创建*****", text_color='red')
        window['state_print'].print(" ")


#  创建脚本文件
class Script(object):
    def __init__(self, Modle_Script_Input_Path, Script_Output_Path, Result_Path):
        self.Modle_Script_Input_Path = Modle_Script_Input_Path
        self.Script_Output_Path = Script_Output_Path
        self.Result_Path = Result_Path

    #  检索替换模块
    def Replacement_module(self, input_path, output_path, input_name, output_name, find_list, replace_list,
                           input_suffix, output_suffix, suffix, index, solve):
        # input_path: 脚本模板路径，output_path: 生成脚本输出路径，input_name：脚本中输入文件名称,output_name：脚本中输出文件名称, find_list:搜索关键词 数组,
        # replace_list: 替换关键词 数组，suffix：保存的脚本后缀,input_suffix:脚本中输入文件后缀,output_suffix：脚本中输出文件后缀
        if solve == 'fluent' or solve == 'fluent_meshing':
            template = open(input_path, 'r', encoding='utf-8')
            generate = open(r"" + output_path + "/" + str(output_name) + suffix, "a", encoding='utf-8')
        else:
            template = open(input_path, 'r')
            generate = open(r"" + output_path + "/" + str(output_name) + suffix, "a")
        for line in template:
            if solve == "fluent_meshing":
                if "输入" in line:
                    line = line.replace("输入", self.Result_Path + '/' + input_name + input_suffix)  # 输入文件的路径
                if "输出" in line:
                    line = line.replace("输出",
                                        self.Result_Path + '/' + output_name + output_suffix)  # 结果文件路径，如.msh 文件 , cadt 文件
                if "统计" in line:
                    line = line.replace("统计",
                                        self.Result_Path + '/' + output_name + '.txt')  # 网格统计文件路径

            if solve == "fluent":
                if "温度单位" in line:
                    line = line.replace("温度单位", values['温度单位'].lower())
                if "环境温度" in line:
                    if values['温度单位'] == 'K':
                        line = line.replace("环境温度", str(float(values['环境温度']) + 273.15))
                    else:
                        line = line.replace("环境温度", values['环境温度'])
                if "迭代次数" in line:
                    line = line.replace("迭代次数", values['迭代次数'])
                if "输入" in line:
                    line = line.replace("输入", self.Result_Path + '/' + input_name + input_suffix)  # 输入文件的路径
                if "输出" in line:
                    line = line.replace("输出",
                                        self.Result_Path + '/' + output_name + output_suffix)  # 结果文件路径，如.msh 文件 ,cadt 文件
                for i in range(len(find_list)):
                    if find_list[i] in line:
                        line = line.replace(find_list[i], replace_list[i])
            if solve == "cfd_post":
                if "温度单位" in line:
                    line = line.replace("温度单位", values['温度单位'])
                if "结果文件路径" in line:
                    line = line.replace("结果文件路径", os.path.dirname(values['规划表路径']) + '/Result.csv')
                if "序号" in line:
                    line = line.replace("序号", index)
                if "输入" in line:
                    line = line.replace("输入", self.Result_Path + '/' + input_name + input_suffix)  # 输入文件的路径
                if "输出" in line:
                    line = line.replace("输出",
                                        self.Result_Path + '/' + output_name + output_suffix)  # 结果文件路径，如.msh 文件 ,cadt 文件
            generate.write(line)
        template.close()
        generate.close()
        sg.cprint("已生成： " + output_name + suffix + " 文件")
        window['state_print'].print("已生成： " + output_name + suffix + " 文件", text_color='red')

    #  创建Fluent_Meshing脚本
    def Fluent_Meshing(self):  # 模板脚本的输入路径，模板脚本输出路径
        if RRS_Gdata[0]: # 判断数组是否为空，也就是是否有几何变量。
            for i in range(len(RRS_Gdata)):
                input_name = "Geom-" + '-'.join(RRS_Gdata[i])
                output_name = "Mesh-" + '-'.join(RRS_Gdata[i])
                self.Replacement_module(self.Modle_Script_Input_Path + "/fluent_meshing.txt",self.Script_Output_Path, input_name, output_name, None, None, ".agdb",".msh", ".log", None, 'fluent_meshing')
                progress("网格脚本", len(RRS_Gdata), i+1)

        elif not RRS_Gdata[0]: # 如果几何变量为空，执行下一步
            input_name = "Geom"
            output_name = "Mesh"
            self.Replacement_module(self.Modle_Script_Input_Path + "/fluent_meshing.txt", self.Script_Output_Path,input_name, output_name, None, None, ".agdb", ".msh", ".log", None,'fluent_meshing')
            progress("网格脚本", 1, 1)


    #  创建Fluent脚本
    def Fluent(self):  # 模板脚本的输入路径，模板脚本输出路径
        for i in range(len(index_all)):
            if RRS_Gdata[0] and excel_Wdata[0]:
                replace_list=excel_Wdata[i]
                input_name = "Mesh-" + '-'.join(excel_Gdata[i])
                output_name = "Fluent-{:0>2d}".format(int(index_all[i]))
                self.Replacement_module(self.Modle_Script_Input_Path + "/fluent.txt", self.Script_Output_Path,input_name, output_name, W_name, replace_list, ".msh", "", ".log", None,"fluent")
                progress("Fluent脚本", len(index_all), i + 1)
            elif not RRS_Gdata[0] and excel_Wdata[0]:
                replace_list = excel_Wdata[i]
                input_name = "Mesh"
                output_name = "Fluent-{:0>2d}".format(int(index_all[i]))
                self.Replacement_module(self.Modle_Script_Input_Path + "/fluent.txt",self.Script_Output_Path, input_name, output_name,W_name, replace_list, ".msh", "", ".log", None, "fluent")
                progress("Fluent脚本", len(index_all), i + 1)

            elif RRS_Gdata[0] and not excel_Wdata[0]:
                input_name = "Mesh-" + '-'.join(excel_Gdata[i])
                output_name = "Fluent-{:0>2d}".format(int(index_all[i]))
                self.Replacement_module(self.Modle_Script_Input_Path + "/fluent.txt", self.Script_Output_Path,input_name, output_name, W_name, None, ".msh", "", ".log", None, "fluent")
                progress("Fluent脚本", len(index_all), i + 1)
            else:
                window['state_print'].print("变量必须存在，请重新输入！", text_color='red')


    #  创建CFD_Post脚本
    def CFD_Post(self):
        for i in range(len(index_all)):
            input_name = "Fluent-{:0>2d}".format(int(index_all[i]))
            output_name = "CFD_Post-{:0>2d}".format(int(index_all[i]))
            self.Replacement_module(self.Modle_Script_Input_Path + "/cfd_post.cse", self.Script_Output_Path,
                                    input_name, output_name, None, None, ".dat", "-", ".cse", str(i + 2), "cfd_post")
            progress("后处理脚本", len(index_all), i + 1)


#  运行已生成的脚本文件
class Calculate(object):
    def __init__(self, scripts_output_path, result_output_path,
                 core_num):  # scripts_path：已生成的脚本所在路径 # core_num: 核心数目 # result_path:所有生成文件所在的路径
        self.scripts_path = scripts_output_path
        self.core_num = core_num
        self.result_path = result_output_path
        self.scripts_list = [[], [], []]  # 脚本文件路径 数组
        self.path=values['规划表路径']

    #  搜索已生成的脚本文件
    def Search_Scripts(self, path, suffix, key_word,
                       num):  # path: 已生成脚本所在路径 suffix：脚本后缀 scripts_num: 所有脚本路径所保存在的子数组, key_word:所匹配的关键字
        self.scripts_list[num].clear()
        for root, dirs, files in walk(path):
            for i in files:
                if os.path.isfile(path + '/' + i):
                    if i.endswith(suffix):
                        if key_word in i:
                            self.scripts_list[num].append(join(root, i))
                            window['state_print'].print('已检索到：' + i + ' 文件')
            sorted(self.scripts_list[num])
            return self.scripts_list[num]
    
    #  将结果文件中的数据转移到规划表中
    def Revise_csv(self,num):  # 结果文件所在文件夹路径
        Response_list = []  # 响应数组
        Response_list.clear()
        

        # 从result.csv 文件中读取响应数据并添加进数组Response_list中
        with open(os.path.dirname(self.path) + '/Result.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in csv_reader:
                Response_list.append(i)
        del (Response_list[0])

        # 打开实验规划表路径
        workbook = xlrd.open_workbook(self.path)  # 括号中为文件路径,打开excel数据表
        workbook_copy = copy(workbook)  # 复制一份excel文件
        table = workbook_copy.get_sheet(0)  # 通过索引读取sheet

        # 为单元格设置背景色
        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 5
        # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan,
        # 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal,
        # 22 = Light Gray, 23 = Dark Gray, the list goes on...
        style = xlwt.XFStyle()  # Create the Pattern
        style.pattern = pattern  # Add Pattern to Style

        # 将响应数据写入实验规划表中
        for i in range(int(values['响应数目'])):
            
            table.write(num + 1, int(values['几何变量']) + int(values['物理变量']) + 1 + i, Response_list[num-1][i],
                            style)  # 将响应写入对应单元
        workbook_copy.save(self.path)  # 保存实验规划表
        sg.cprint("第"+str(num)+"组响应值已写入实验规划表中！", text_color='red')
        sg.cprint(" ")
        window['state_print'].print("第"+str(num)+"组响应值已写入实验规划表中！", text_color='red')
        window['state_print'].print(" ")



    def DM(self,):  #
        # 保证ansys workbench与solidworks已关联成功；
        # solidworks 所建模型树命名必须为全英文，solidworks模型为全英文，并且在solidworks中已进行边界命名；

        def run():
            os.system('runwb2 -B')

        def beach():
            while True:
                button_center = pyautogui.locateOnScreen(beach_image)  # 搜索图标的中心坐标
                if button_center != None:
                    break
            return button_center

        def search():
            while True:
                button_center = pyautogui.locateOnScreen(yes_image, region=(0, 1006, 79, 1042))
                if button_center != None:
                    break

        threading.Thread(target=run, daemon=True, ).start()  # 打开workbench命令窗

        pyautogui.doubleClick(beach())  # 通过双击将workbench命令窗置顶
        pyautogui.hotkey('win', 'up')  # 最大化
        time.sleep(0.5)
        pyautogui.hotkey('enter')  # 确定
        pyautogui.hotkey('shift')  # 更改输入法为英文
        time.sleep(0.5)

        # 在workbench命令窗中输入脚本命令，打开DM
        pyautogui.write('template1=GetTemplate(TemplateName="Geometry")\n')
        pyautogui.write('system1=template1.CreateSystem()\n')
        pyautogui.write('geometry1=system1.GetContainer(ComponentName="Geometry")\n')
        pyautogui.write('geometry1.Edit()\n')
        search()  # 搜索“完成”图标：如果打开DM成功进行下一步
        configuration_num = 1  # 构型数目为1
        if G_name[0] == "构型":  # 如果规划表中存在构型这个选项时
            RRS_Gdata1 = np.array(RRS_Gdata)  # 必要numpy矩阵的处理
            RRS_Gdata2 = RRS_Gdata1[:, 0]  # 将第一列选出，也就是构型那一列
            configuration_num = len(RRS_Gdata2)  # 构型的数目



        for i in range(configuration_num):  # 进行遍历构型，修改参数生成对应模型
            pyautogui.click(x=40, y=250)
            pyautogui.hotkey('ctrl', 'N')  # 重置DM
            pyautogui.hotkey('Y')  # 确定
            time.sleep(1)
            # 导入外部几何模型
            pyautogui.click(x=21, y=33)  # 点击文件
            pyautogui.click(x=90, y=185)  # 点击导入外部几何模型
            time.sleep(0.5)
            pyautogui.hotkey('backspace')  # 清空文件输入栏
            time.sleep(0.5)
            if G_name[0] == "构型":  # 如果为多构型时
                pyautogui.write(result_path + '\Geom-' + str(RRS_Gdata2[i]) + '.SLDPRT')  # 导入模板模型
            else:  # 如果为单个构型
                pyautogui.write(result_path + '\Geom.SLDPRT')  # 导入模板模型
            pyautogui.hotkey('enter')  # 确认

            # 设置命名选择
            time.sleep(1)
            pyautogui.doubleClick(x=142, y=911)  # 双击将命名选择设置为是
            pyautogui.hotkey('F5')  # 生成
            time.sleep(1)
            search()  # 搜索“完成”图标：表示模型导入成功

            if G_name[0] == "构型":  # configuration_i_list为每个构型所对应的几何参数所构成的数组
                configuration_i_list = RRS_Gdata1[tuple([RRS_Gdata2 == str(float(i + 1))])]  # 从几何参数中筛选出指定构型的几何参数
                configuration_i_list1 = configuration_i_list[:, 1:]  # 剔除第一列，将剩下的几何参数构成矩阵
            else:
                configuration_i_list1 = RRS_Gdata  # 单个构型的就是整个原始几何参数矩阵全是几何参数
            sg.cprint('结果')

            for h in range(len(configuration_i_list1)):  # 遍历几何参数矩阵，以生成模型
                # 修改几何参数
                for i in range(len(configuration_i_list1[h])):  # 进行循环修改模板模型中的所有参数
                    pyautogui.click(x=93, y=229)  # 点击“导入”
                    for j in range(40):
                        pyautogui.click(x=467, y=1001)  # 点击滚动的向下滚动
                    time.sleep(1)
                    pyautogui.click(198, 995 - i * 22)  # 从下往上依次点击要修改的属性
                    pyautogui.hotkey('backspace')  # 清空输入框
                    pyautogui.write(configuration_i_list1[h][len(configuration_i_list1[h]) - i - 1])  # 输入要修改的参数
                    time.sleep(0.5)

                pyautogui.hotkey('enter')
                pyautogui.hotkey('F5')  # 更新并生成
                search()  # 搜索“完成”图标：表示更新导入成功

                # Part 重命名
                pyautogui.click(x=40, y=250)
                pyautogui.click(x=110, y=275)
                pyautogui.click(x=115, y=640)
                pyautogui.hotkey('backspace')  #
                pyautogui.write('part')  # 输入修改的part名称
                pyautogui.hotkey('enter')

                # 保存文件
                time.sleep(1)
                pyautogui.click(pyautogui.locateOnScreen(save_image))  # 搜索另存为图标并点击
                time.sleep(0.5)
                pyautogui.hotkey('backspace')  # 清空文件输入栏
                time.sleep(0.5)
                if G_name[0] == "构型":
                    pyautogui.write(result_path + "\Geom-" + '-'.join(configuration_i_list1[h]))  # 保存文件路径及文件名
                else:
                    pyautogui.write(result_path + "\Geom-" + '-'.join(configuration_i_list1[h]))  # 保存文件路径及文件名
                pyautogui.hotkey('enter')  # 确认
                time.sleep(2)
                pyautogui.hotkey('Y')  # 确定
                sg.cprint('已生成： Geom-' + '-'.join(configuration_i_list1[h]) + '.agdb 文件')
                window['state_print'].print('已生成： Geom-' + '-'.join(configuration_i_list1[h]) + '.agdb 文件', text_color='red')
                window['state_print'].print(" ")

        # 关闭DM
        pyautogui.click(x=21, y=33)  # 点击文件
        pyautogui.click(x=50, y=386)  # 关闭DesignModel
        # 关闭workbench命令窗
        pyautogui.doubleClick(beach())  # 搜索并双击符号“<<<”
        pyautogui.click(x=1896, y=7)  # 点击X 关闭workbench命令窗
        time.sleep(10)  # 等待workbench命令窗完全关闭



    # 运行Fluent_Meshing脚本 #
    def Fluent_Meshing(self):
        self.Search_Scripts(self.scripts_path, ".log", "Mesh-", 0)  # 检索fluent meshing脚本，并添加进数组中
        for i in range(len(self.scripts_list[0])):
            progress("网格划分", len(self.scripts_list[0]), i + 1)
            command = f"fluent 3d -meshing -tm{self.core_num} -t{self.core_num} -g -wait -i {self.scripts_list[0][i]}"
            com = str(command + " &&exit")
            a = subprocess.Popen(com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, text=True)
            for u in iter(a.stdout.readline, b""):
                window['state_print'].print('{:0>2d}* '.format(i + 1) + u.decode().strip())
            name = os.path.basename(self.scripts_list[0][i])
            name = name.split('.m')[0]
            sg.cprint('已生成： ' + str(name) + '.msh 文件')
            window['state_print'].print('已生成： ' + str(name) + '.msh 文件', text_color='red')
            window['state_print'].print(" ")

    # 运行Fluent脚本
    def Fluent(self):
        if os.path.exists(self.scripts_path + '/Fluent终端记录.txt'):
            os.remove(self.scripts_path + '/Fluent终端记录.txt')
        open(self.scripts_path + '/Fluent终端记录.txt', 'w').close()
        self.Search_Scripts(self.scripts_path, ".log", "Fluent-", 1)  # 检索fluent脚本，并添加进数组中
        for i in range(len(self.scripts_list[1])):
            progress("求解计算", len(self.scripts_list[1]), i + 1)
            command = f"fluent 3d -t{self.core_num} -g -wait -i {self.scripts_list[1][i]}" # 3ddp为双精度
            com = str(command + " &&exit")
            a = subprocess.Popen(com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, text=True)  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
            terminal_record = open(self.scripts_path + '/Fluent终端记录.txt', 'a+', encoding='utf-8')
            for u in iter(a.stdout.readline, b""):
                window['state_print'].print('{:0>2d}* '.format(i + 1) + u.decode().strip())
                txt = str(u.decode().strip())
                terminal_record.write(txt + "\n")
            terminal_record.close()
            name = os.path.basename(self.scripts_list[1][i])
            name = name.split('.')[0]
            sg.cprint('已生成： ' + name + '.dat 文件 与 ' + name + '.cas 文件')
            window['state_print'].print('已生成： ' + name + '.dat 文件 与 ' + name + '.cas 文件', text_color='red')
            window['state_print'].print(" ")
            
            
    

    # 批量运行CFD_Post脚本 #
    def CFD_Post(self):  # 批量进行后处理
        self.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        for i in range(len(self.scripts_list[2])):
            (filename,extension) = os.path.splitext(self.scripts_list[2][i])
            print(filename)
            pattern_num=int(filename.split('Post-')[1])
            window['state_print'].print("********** 开始进行第" + str(pattern_num) + "组后处理 **********", text_color='red')
            progress("Post后处理", len(self.scripts_list[2]), i+1)
            command = "cfdpost -batch " + self.scripts_list[2][i]
            com = str(command + " &&exit")
            a = subprocess.Popen(com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL)  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
            for u in iter(a.stdout.readline, b""):
                window['state_print'].print('{:0>2d}* '.format(pattern_num) + u.decode().strip())
            sg.cprint('已完成 ' + str(pattern_num) + ' 组后处理', text_color='red')
            window['state_print'].print('已完成 ' + str(pattern_num) + ' 组后处理', text_color='red')
            self.Revise_csv(pattern_num) # 将结果文件数据转移到实验规划表中
            window['state_print'].print(" ")
        

    # 即时运行CFD_Post脚本子方法 #
    def CFD_Post_Alone(self, num, all_num):
        window['state_print'].print("********** 开始进行第" + str(num+1) + "组后处理 **********", text_color='red')
        command = "cfdpost -batch " + self.scripts_list[2][num]
        com = str(command + " &&exit")
        a = subprocess.Popen(com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL)  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
        for u in iter(a.stdout.readline, b""):
            window['state_print'].print('{:0>2d}* '.format(num+1) + u.decode().strip())
        sg.cprint("********** 已完成第 " + str(num+1) + " 组后处理 **********", text_color='red')
        window['state_print'].print("{:0>2d}组数据已写入Result.csv".format(num+1), text_color='red')
        window['state_print'].print(" ")
        self.Revise_csv(num+1) # 将结果文件保存到实验规划表中
        window['state_print'].print("已完成： 第" + str(num+1) + " 组后处理", text_color='red')
        window['state_print'].print(" ")
        window['state_print'].print("----------------------------------------------------------")
        window['state_print'].print(" ")
        if str(all_num) == str(num+1):
            window['state_print'].print('本次运行结束', text_color='red')
            sg.cprint('本次运行结束', text_color='red')

    # 即时运行CFD_Post脚本总方法 #
    def CFD_Post_Immediate(self):
        scripts_num = len(self.scripts_list[2])
        
        for j in range(len(self.scripts_list[2])):
            (filename,extension) = os.path.splitext(self.scripts_list[2][j])
            pattern_num=int(filename.split('Post-')[1]) # 从脚本路径中选出需要匹配的序号
            while True:
                pattern = re.compile("Fluent-{:0>2d}".format(pattern_num)+'.plt')
                for root, dirs, files in walk(self.result_path):
                    for i in files:
                        if re.match(pattern, i):
                            break
                    else:
                        continue
                    break
                else:
                    time.sleep(1)
                    continue
                break
            time.sleep(20)
            threading.Thread(target=self.CFD_Post_Alone, args=(j, scripts_num,), daemon=True, ).start()


class Run(object):
    def __init__(self, time_start, scripts_output_path, result_output_path):
        self.scripts_path = scripts_output_path
        self.result_path = result_output_path
        self.time_start = int(time_start)
        self.time_stop = False

    #  更新时间
    def update_time(self):
        while True:
            time_end = int(time.time())
            time_run = time_end - int(self.time_start)
            window['运行时间'].update(
                value=str((time_run // 60 // 60)) + "小时 " + str(int(time_run // 60 % 60)) + "分钟 " + str(
                    round(time_run % 60)) + "秒")
            time.sleep(0.2)
            if self.time_stop is True:
                break
    def DM_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.result_path, ".agdb", "Geom")
        Class_Calculate.DM()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent_Meshing_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        Class_Script.Fluent_Meshing()
        Class_Calculate.Fluent_Meshing()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        Class_Script.Fluent()
        Class_Calculate.Fluent()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def CFD_Post_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".cse", "CFD_Post")
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        Class_Script.CFD_Post()
        Class_Calculate.CFD_Post()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def DM_Mesh_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        SearchFile_remove(self.result_path, ".agdb", "Geom")
        Class_Calculate.DM()
        Class_Script.Fluent_Meshing()
        Class_Calculate.Fluent_Meshing()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')


    def Mesh_Fluent_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        Class_Script.Fluent_Meshing()
        Class_Script.Fluent()
        Class_Calculate.Fluent_Meshing()
        Class_Calculate.Fluent()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent_Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        SearchFile_remove(self.scripts_path, ".cse", "CFD_Post")
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        Class_Script.Fluent()
        Class_Script.CFD_Post()
        Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        Class_Calculate.Fluent()
        self.time_stop = True

    def DM_Mesh_fluent(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        SearchFile_remove(self.result_path, ".agdb", "Geom")
        Class_Calculate.DM()
        Class_Script.Fluent_Meshing()
        Class_Script.Fluent()
        Class_Calculate.Fluent_Meshing()
        Class_Calculate.Fluent()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Mesh_Fluent_Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        SearchFile_remove(self.scripts_path, ".cse", "CFD_Post")
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        Class_Script.Fluent_Meshing()
        Class_Script.Fluent()
        Class_Script.CFD_Post()
        Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        Class_Calculate.Fluent_Meshing()
        Class_Calculate.Fluent()
        self.time_stop = True


    def DM_Mesh_Fluent_Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        SearchFile_remove(self.scripts_path, ".cse", "CFD_Post")
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        SearchFile_remove(self.result_path, ".agdb", "Geom")
        Class_Calculate.DM()
        Class_Script.Fluent_Meshing()
        Class_Script.Fluent()
        Class_Script.CFD_Post()
        Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        Class_Calculate.Fluent_Meshing()
        Class_Calculate.Fluent()
        self.time_stop = True

    def Only_Fluent_Meshing_Run(self): # 不生成脚本文件，使用已有的脚本
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        Class_Calculate.Fluent_Meshing()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Only_Fluent_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        Class_Calculate.Fluent()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Only_CFD_Post_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        Class_Calculate.CFD_Post()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Nos_Fluent_Post(self):  # 直接使用已生成的脚本
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        Class_Calculate.Fluent()
        self.time_stop = True

    def Nos_Mesh_Fluent_Post(self):  # 直接使用已生成的脚本
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.result_path, ".msh", "Mesh")
        SearchFile_remove(self.result_path, ".cas", "Fluent")
        SearchFile_remove(self.result_path, ".dat", "Fluent")
        SearchFile_remove(self.result_path, ".plt", "Fluent")
        SearchFile_remove(self.result_path, ".png", "CFD_Post")
        Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        Class_Calculate.Fluent_Meshing()
        Class_Calculate.Fluent()
        self.time_stop = True



    def Fluent_Meshing_Script(self): # 只生成脚本文件
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Mesh")
        Class_Script.Fluent_Meshing()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent_Script(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".log", "Fluent")
        Class_Script.Fluent()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def CFD_Post_Script(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchFile_remove(self.scripts_path, ".cse", "CFD_Post")
        Class_Script.CFD_Post()
        self.time_stop = True
        window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')


sg.theme('darkbrown4')
# 2) 定义布局，确定行数

Calculation_settings_layout = sg.Frame('计算设置', [

    [sg.Text('几何变量：', size=(8, 1), pad=((10, 0), (15, 0))),
     sg.In(default_text='', key='几何变量', tooltip='指改变几何模型的因素数量', size=(8, 1), pad=((10, 0), (15, 0)),
           justification='center', focus=True), ],
    [sg.Text('物理变量：', size=(8, 1), pad=((10, 0), (8, 0))),
     sg.In(default_text='', key='物理变量', tooltip='指改变不改变几何模型的因素数量', size=(8, 1), pad=((10, 0), (8, 0)),
           justification='center'), ],
    [sg.Text('响应数目：', size=(8, 1), pad=((10, 0), (8, 0))),
     sg.In(default_text='', key='响应数目', tooltip='指计算所得响应的数目', size=(8, 1), pad=((10, 0), (8, 0)),
           justification='center'), ],

    [sg.Text('核心数目：', size=(8, 1), pad=((10, 0), (8, 0))),
     sg.In(default_text='50', key='核心数目', tooltip='请输入数字', size=(8, 1), pad=((10, 0), (8, 0)), justification='center')],
    [sg.Text('迭代次数：', size=(8, 1), pad=((10, 0), (8, 0))),
     sg.In(default_text='500', key='迭代次数', tooltip='请输入数字', size=(8, 1), pad=((10, 0), (8, 0)),
           justification='center')],

    [sg.Text('温度单位：', size=(8, 1), pad=((10, 0), (8, 0))),
     sg.Combo(list('KC'), key='温度单位', readonly=True, default_value='K', size=(6, 1), pad=((10, 0), (8, 0)))],
    [sg.Text('环境温度：', size=(8, 1), pad=((10, 0), (8, 0))),
     sg.In(default_text='25', key='环境温度', size=(8, 1), pad=((10, 0), (8, 0)), justification='center',
           tooltip='自动换算成单位选项所设单位'), sg.Text('摄氏度', size=(7, 1), pad=((10, 5), (8, 0)))],
    [sg.Checkbox('Design Model  修改创建模型', key='DM修改', size=(22, 1), pad=((10, 0), (20, 0)))],
    [sg.Checkbox('Mesh  生成', key='Mesh生成', size=(8, 1), pad=((10, 0), (5, 0))),
     sg.Checkbox('Mesh  脚本', key='Mesh脚本', size=(8, 1), pad=((10, 10), (5, 0)))],
    [sg.Checkbox('Fluent 求解', key='Fluent求解', size=(8, 1), pad=((10, 0), (5, 0))),
     sg.Checkbox('Fluent 脚本', key='Fluent脚本', size=(8, 1), pad=((10, 10), (5, 0)))],
    [sg.Checkbox('Post   处理', key='Post处理', size=(8, 1), pad=((10, 0), (5, 0))),
     sg.Checkbox('Post   脚本', key='Post脚本', size=(8, 1), pad=((10, 10), (5, 0)))],

    [sg.Button('全选', size=(10, 1), pad=((15, 0), (20, 0))), sg.Button('清空', size=(10, 1), pad=((10, 15), (20, 0)))],
    [sg.Button('运行', key='运行', disabled=False, size=(22, 1), pad=((15, 0), (20, 0))), ],
    [sg.Button('清除', size=(22, 1), pad=((15, 15), (10, 20)))]
], border_width=2, pad=((10, 10), (10, 10)))

Path_Settings_layout = [
    [sg.Text('开始时间：', size=(8, 1), pad=((10, 0), (20, 0))),
     sg.In(default_text='程序开始时间', key='开始时间', size=(21, 1), pad=((5, 0), (20, 0)), justification='center'),
     sg.Text('规划表路径：', size=(11, 1), pad=((25, 0), (20, 0))),
     sg.In(key='规划表路径', disabled=False, tooltip='选定实验规划表', size=(70, 1), pad=((10, 0), (20, 0))),
     sg.FileBrowse('  浏览  ', initial_folder=os.path.dirname(sys.argv[0]), key='规划表路径按钮', pad=((20, 0), (20, 0)), )],

    [sg.Text('运行时间：', size=(8, 1), pad=((10, 0), (4, 0))),
     sg.In(default_text='程序运行时间', key='运行时间', size=(21, 1), pad=((5, 0), (4, 0)), justification='center'),
     sg.Text('脚本模板路径：', size=(11, 1), pad=((25, 0), (4, 0))),
     sg.In(key='脚本模板路径', disabled=False, tooltip='脚本所在文件夹', size=(70, 1), pad=((10, 0), (4, 0))),
     sg.FolderBrowse("  浏览  ", initial_folder=os.path.dirname(sys.argv[0]), key='脚本模板路径按钮', pad=((20, 0), (4, 0)), )],
]

Show_layout = sg.TabGroup([
    [sg.Tab('运行状态', [
        [sg.Text('运行进度：', key='进度名称', size=(10, 1), pad=((5, 0), (4, 0)), auto_size_text=True, justification='center'),
         sg.In(default_text='', key='进度', size=(75, 1), pad=((5, 0), (4, 0)), justification='left'),
         sg.Text('0%', key='百分比', size=(5, 1), pad=((0, 0), (4, 0)), justification='center')], [
            sg.Multiline(default_text='', key='state_print', size=(90, 26), pad=((0, 0), (5, 0)), reroute_stdout=True,
                         background_color='black', text_color='green', )]]),
     sg.Tab('结果显示', [[sg.Multiline(default_text='', size=(90, 27), reroute_cprint=True, key='result_print',
                                   pad=((0, 0), (13, 0)), background_color='black', text_color='green')]]),
     sg.Tab('使用说明', [[sg.Multiline(default_text=manual, size=(79, 27), key='manual', pad=((0, 0), (13, 0)), font='宋体',
                                   background_color='light gray', text_color='black')]]),
     ]], title_color='red', tab_background_color='black', selected_title_color='white', selected_background_color='red',
    pad=((10, 10), (10, 10)))

all_layout = [Path_Settings_layout], [Calculation_settings_layout, Show_layout]

layout = [all_layout]


# 3) 创建窗口
window = sg.Window('CFD Automatic Simulation Software by YanMing', layout, icon='CASS-Resource/CASS-logo.ico', finalize=True)

# 4) 事件循环
while True:
    event, values = window.read()  # 窗口的读取，有两个返回值(1.事件  2.值)

    if event is None:  # 窗口关闭事件

        break

    if event == '全选':
        window['Mesh生成'].update(value=True)
        window['Fluent求解'].update(value=True)
        window['Post处理'].update(value=True)

    if event == '清空':
        window['Mesh脚本'].update(value=False)
        window['Mesh生成'].update(value=False)
        window['Fluent脚本'].update(value=False)
        window['Fluent求解'].update(value=False)
        window['Post脚本'].update(value=False)
        window['Post处理'].update(value=False)

    if event == '运行':
        window['state_print'].update('')
        window['result_print'].update('')
        window['开始时间'].update(value=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))))
        window['规划表路径按钮'].update(disabled=True, )
        window['脚本模板路径按钮'].update(disabled=True, )
        window['运行'].update(disabled=True, )

        sg.cprint('准备工作已完成，开始进行计算处理', text_color='red')
        if values['规划表路径'] == '' or values['脚本模板路径'] == '' or values['几何变量'] == '' or values['物理变量'] == '' or values[
            '物理变量'] == '响应数目':
            window['state_print'].print('请检查是否输入实验规划表路径、脚本模板路径、集合变量、物理变量、响应数目！', text_color='red')
        else:
            Class_Prepare = Prepare(values['规划表路径'], scripts_path, result_path)  # 初始化 准备工作类
            Class_Prepare.excel(int(values['几何变量']), int(values['物理变量']), int(values['响应数目']))  # 读取excel
            Class_Prepare.create_folder()  # 创建文件夹
            Class_Prepare.create_csv()  # 创建空白结果文件
            Class_Script = Script(values['脚本模板路径'], scripts_path, result_path)  # 初始化脚本生成类
            Class_Calculate = Calculate(scripts_path, result_path, values['核心数目'])
            Class_Run = Run(int(time.time()), scripts_path, result_path)

            # 同时运行四个模块,包括脚本生成
            if values['DM修改']is True and values['Mesh脚本'] is True and values['Fluent脚本'] is True and values['Post脚本'] is True and values[
                'Mesh生成'] is True and values['Fluent求解'] is True and values['Post处理'] is True:
                threading.Thread(target=Class_Run.DM_Mesh_Fluent_Post(), daemon=True, ).start()

            # 同时运行三个模块，包括脚本的生成
            elif values['DM修改']is True and values['Mesh脚本'] is True and values['Fluent脚本'] is True and values['Post脚本'] is False and values[
                'Mesh生成'] is True and values['Fluent求解'] is True and values['Post处理'] is False:
                threading.Thread(target=Class_Run.DM_Mesh_fluent, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is True and values['Fluent脚本'] is True and values['Post脚本'] is True and values[
                'Mesh生成'] is True and values['Fluent求解'] is True and values['Post处理'] is True:
                threading.Thread(target=Class_Run.Mesh_Fluent_Post, daemon=True, ).start()

            # 同时运行两个模块，包括脚本的生成
            elif values['DM修改']is True and values['Mesh脚本'] is True and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is True and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.DM_Mesh_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is True and values['Fluent脚本'] is True and values['Post脚本'] is False and values[
                'Mesh生成'] is True and values['Fluent求解'] is True and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Mesh_Fluent_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is True and values['Post脚本'] is True and values[
                'Mesh生成'] is False and values['Fluent求解'] is True and values['Post处理'] is True:
                threading.Thread(target=Class_Run.Fluent_Post, daemon=True, ).start()

            # 单独运行单个模块，包括脚本生成
            elif values['DM修改']is True and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.DM_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is True and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is True and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Fluent_Meshing_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is True and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is True and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Fluent_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is True and values[
                'Mesh生成'] is False and values['Fluent求解'] is False and values['Post处理'] is True:
                threading.Thread(target=Class_Run.CFD_Post_Run, daemon=True, ).start()

            # 运行单个模块，不生成脚本
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is True and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Only_Fluent_Meshing_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is True and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Only_Fluent_Run, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is False and values['Post处理'] is True:
                threading.Thread(target=Class_Run.Only_CFD_Post_Run, daemon=True, ).start()

            # 运行两个模块，不生成脚本
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is True and values['Post处理'] is True:
                threading.Thread(target=Class_Run.Nos_Fluent_Post, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is True and values['Fluent求解'] is True and values['Post处理'] is True:
                threading.Thread(target=Class_Run.Nos_Mesh_Fluent_Post, daemon=True, ).start()


            elif values['DM修改']is False and values['Mesh脚本'] is True and values['Fluent脚本'] is False and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Fluent_Meshing_Script, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is True and values['Post脚本'] is False and values[
                'Mesh生成'] is False and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.Fluent_Script, daemon=True, ).start()
            elif values['DM修改']is False and values['Mesh脚本'] is False and values['Fluent脚本'] is False and values['Post脚本'] is True and values[
                'Mesh生成'] is False and values['Fluent求解'] is False and values['Post处理'] is False:
                threading.Thread(target=Class_Run.CFD_Post_Script, daemon=True, ).start()
            else:
                window['state_print'].print(f'Error： 文件被占用，清除失败！\n地址：{os.path.dirname(sys.argv[0])}\n请解除！', text_color='red')

    if event == '清除':
        window['运行'].update(disabled=False, )
        window['脚本模板路径按钮'].update(disabled=False, )
        window['规划表路径按钮'].update(disabled=False, )
        try:
            SearchFile_remove(os.path.dirname(sys.argv[0]), ".trn", "任意")
            SearchFile_remove(os.path.dirname(sys.argv[0]), ".bat", "任意")
            SearchFile_remove(os.path.dirname(sys.argv[0]), ".log", "任意")
        except WindowsError:
            window['state_print'].print('Error： 文件被占用，清除失败！\n请后台关闭相关程序后，再尝试清除！', text_color='red')

window.close()

# 日志 
# V4.1.0  2022/8/18 19:44
# 优化了即时后处理模块，解决了只能按照从1开始执行后处理的问题，以后可以完美即时运行后
# 处理了。

# V4.1.1 2022/8/19 9:47
# 修改了即时后处理程序，检索匹配关键序号不对的bug。 

# V4.1.2 2022/8/25 19:50
# 发现CFDPost在读取excel时会自动将数字用科学计数法保留两位小数，这导致数据的精度不够。因此做了一些改动，将原先的全部后处理完再转移数据的形式，改为每处理完一组就进行数据转移至实验规划表。

# V4.1.3 2023/6/10 20:48
# 尝试解决Fluent 2023R1 打印不出控制台信息的问题 主要修改subprocess.Popen命令
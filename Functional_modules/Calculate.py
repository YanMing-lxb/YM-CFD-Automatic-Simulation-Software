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
Date         : 2023-07-25 10:15:12 +0800
LastEditTime : 2024-07-30 14:56:58 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /YM-CFD-Automatic-Simulation-Software/Functional_modules/Calculate.py
Description  : 
 -----------------------------------------------------------------------
'''

import re
import os
import sys
import csv
import xlrd
import xlwt
import time

import base64
from PIL import Image
from io import BytesIO
import pyautogui

import threading
import subprocess
import numpy as np
import PySimpleGUI as sg
from xlutils.copy import copy

from Functional_modules.Progress import Progress

content_beach = """iVBORw0KGgoAAAANSUhEUgAAABgAAAAPCAYAAAD+pA/bAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAABmSURBVDhP1ZRBCsAgDATTnvOoPD0/a9kggqQKxezBuYhs2AEDXqr6CJG7nTRC4O5xmbGTh8DMlkM7eX8ilmTYAUOSllwtSQJQKfkUIMTQjD95ElSWg0FQXQ66gFEOQsAqB6d/diIv1qNjI1hTIysAAAAASUVORK5CYII="""
content_save = """iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAHcSURBVDhPrVTNK0RRFD8j/4CVrCRZaGxYKo2FBYqoKQuFhWg2iAUrayVZKrGYWSgfpbCRka+yYCHlOytWdrOf+95zfufc613TsOHUfefjnvs7v3PunUkUCoWI/kEEaHnjhcIooqIJyQSh6KKJxDZWS6zEN4Ge2VtKUSXQANJcXUOXb++0OBlyBCRZJ6z+WrHfkYmos76Bdh8e2ScFAmpo0ZF8MZ6j0BiKeIXFoi7P7zqckNzd8zUyVa2AUCBQDUIAacW21UHR8fKZqa1tB7a4xyhgRthEO6dD62WZwMbqOZuW+fS0jtLW3b0PFDEQM7OM2nPDossxcbaMQ7qA77WGoDDixHx6pSwTF+u7mpVcKc7MIArETGJ0vpGdMdGu+jc7ofaPjDCjVG0d9c+8io8E907g+zZ0ujEZz5VFHmRm4VpAUAHPAAm4RVBHTHxeansx1tmbW3re7rXDZlQHsv/08isT5w8km7y358+Ig0qVNz8uOMaH5J0YsfOb8zwiHWzLyJHN17FAKvCB46hK1RIQaAeCL4oBJH7EFgiH3UyknRIQ+BA5Yn/cmh8P296agmBOsA+yc7LpDvo2tOtA8hkU8vV/1D11IiDSGieqjv3ve8oEIDhcOB6Igf4mRJ/SoWmfLfO/ggAAAABJRU5ErkJggg=="""
content_yes = """iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAEjSURBVDhPrZThsYIwEISjw//XhB1gB68IOrAEi6AD7cAi6EA7sAx+MuPLbm7DkYDvh26G4ZJcPpZwYTeO4yt8QQRN02TdWbefp0WP2Hij+kOXAqemaWrQDEgyTAxyFNrYPLACAYIkCMvYIqAShmLacOjZXYA85BqbAB6k+aRHaFs46wna22iWILq84PB+ujBi380TpH3Rq5QA6XW6845ZXefnGUNLRwBtSZBSeqaB6CW7KRf5/u56tCiKkEQiaM2HFm9CCiVHIK3sy1tIkZ73SOP4xOWid05UEgStlb0Wr0Kcm75LRZkdkWwJKrv/IChIaXFEflETtlcuP6kYAGPoBsZVZePs+KdQAFSQNkOkzd8IKjaZmyl4fe2JVz601v9AIfwBWyytn1UYFGIAAAAASUVORK5CYII="""

beach_image=Image.open(BytesIO(base64.b64decode(content_beach.encode("utf8"))))
save_image=Image.open(BytesIO(base64.b64decode(content_save.encode("utf8"))))
yes_image=Image.open(BytesIO(base64.b64decode(content_yes.encode("utf8"))))

#  运行已生成的脚本文件
class Calculate(Progress):
    def __init__(self,window, PathTable,scripts_output_path, result_output_path,
                 NumCore,NumVarGeom,NumVarPhy,NumRes,G_name,RRS_Gdata ):  # scripts_path：已生成的脚本所在路径 # NumCore: 核心数目 # result_path:所有生成文件所在的路径
        self.window = window
        self.scripts_path = scripts_output_path
        self.NumCore = NumCore
        self.result_path = result_output_path
        self.PathTable = PathTable
        self.NumVarGeom=NumVarGeom
        self.NumVarPhy=NumVarPhy
        self.NumRes=NumRes
        self.G_name=G_name
        self.RRS_Gdata=RRS_Gdata
        self.scripts_list = [[], [], []]  # 脚本文件路径 数组
        

    #  搜索已生成的脚本文件
    def Search_Scripts(self, path, suffix, key_word,
                       num):  # path: 已生成脚本所在路径 suffix：脚本后缀 scripts_num: 所有脚本路径所保存在的子数组, key_word:所匹配的关键字
        self.scripts_list[num].clear()
        for root, dirs, files in os.walk(path):
            for i in files:
                if os.path.isfile(path + '/' + i):
                    if i.endswith(suffix):
                        if key_word in i:
                            self.scripts_list[num].append(os.path.join(root, i))
                            self.window['state_print'].print('已检索到：' + i + ' 文件')
            sorted(self.scripts_list[num])
            return self.scripts_list[num]
    
    #  将结果文件中的数据转移到规划表中
    def Revise_csv(self,num):  # 结果文件所在文件夹路径
        Response_list = []  # 响应数组
        Response_list.clear()
        

        # 从result.csv 文件中读取响应数据并添加进数组Response_list中
        with open(os.path.dirname(self.PathTable) + '/Result.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in csv_reader:
                Response_list.append(i)
        del (Response_list[0])

        # 打开实验规划表路径
        workbook = xlrd.open_workbook(self.PathTable)  # 括号中为文件路径,打开excel数据表
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
        for i in range(int(self.RRS_Gdata)):
            
            table.write(num + 1, int(self.NumVarGeom) + int(self.NumVarPhy) + 1 + i, Response_list[num-1][i],
                            style)  # 将响应写入对应单元
        workbook_copy.save(self.PathTable)  # 保存实验规划表
        sg.cprint("第"+str(num)+"组响应值已写入实验规划表中！", text_color='red')
        sg.cprint(" ")
        self.window['state_print'].print("第"+str(num)+"组响应值已写入实验规划表中！", text_color='red')
        self.window['state_print'].print(" ")



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
        if self.G_name[0] == "构型":  # 如果规划表中存在构型这个选项时
            RRS_Gdata1 = np.array(self.RRS_Gdata)  # 必要numpy矩阵的处理
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
            if self.G_name[0] == "构型":  # 如果为多构型时
                pyautogui.write(self.result_path + '\Geom-' + str(RRS_Gdata2[i]) + '.SLDPRT')  # 导入模板模型
            else:  # 如果为单个构型
                pyautogui.write(self.result_path + '\Geom.SLDPRT')  # 导入模板模型
            pyautogui.hotkey('enter')  # 确认

            # 设置命名选择
            time.sleep(1)
            pyautogui.doubleClick(x=142, y=911)  # 双击将命名选择设置为是
            pyautogui.hotkey('F5')  # 生成
            time.sleep(1)
            search()  # 搜索“完成”图标：表示模型导入成功

            if self.G_name[0] == "构型":  # configuration_i_list为每个构型所对应的几何参数所构成的数组
                configuration_i_list = RRS_Gdata1[tuple([RRS_Gdata2 == str(float(i + 1))])]  # 从几何参数中筛选出指定构型的几何参数
                configuration_i_list1 = configuration_i_list[:, 1:]  # 剔除第一列，将剩下的几何参数构成矩阵
            else:
                configuration_i_list1 = self.RRS_Gdata  # 单个构型的就是整个原始几何参数矩阵全是几何参数
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
                if self.G_name[0] == "构型":
                    pyautogui.write(self.result_path + "\Geom-" + '-'.os.path.join(configuration_i_list1[h]))  # 保存文件路径及文件名
                else:
                    pyautogui.write(self.result_path + "\Geom-" + '-'.os.path.join(configuration_i_list1[h]))  # 保存文件路径及文件名
                pyautogui.hotkey('enter')  # 确认
                time.sleep(2)
                pyautogui.hotkey('Y')  # 确定
                sg.cprint('已生成： Geom-' + '-'.os.path.join(configuration_i_list1[h]) + '.agdb 文件')
                self.window['state_print'].print('已生成： Geom-' + '-'.os.path.join(configuration_i_list1[h]) + '.agdb 文件', text_color='red')
                self.window['state_print'].print(" ")

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
            self.progress("网格划分", len(self.scripts_list[0]), i + 1)
            command = f"fluent 3d -meshing -tm{self.NumCore} -t{self.NumCore} -g -wait -i {self.scripts_list[0][i]} &&exit"
            a = subprocess.Popen(command, 
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT,
                                encoding=sys.getdefaultencoding(), # 使用默认编码
                                errors='replace'  # 替换无法解码的字符
                                )  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
            while a.poll() is None:
                line = a.stdout.readline()
                self.window['state_print'].print('{:0>2d}* '.format(i + 1) + line)
            name = os.path.basename(self.scripts_list[0][i])
            name = name.split('.m')[0]
            sg.cprint(f'已生成：{name}.msh 文件')
            self.window['state_print'].print(f'已生成：{name}.msh 文件', text_color='red')
            self.window['state_print'].print(" ")

    # 运行Fluent脚本
    def Fluent(self):
        if os.path.exists(f'{self.scripts_path}/Fluent终端记录.txt'):
            os.remove(f'{self.scripts_path}/Fluent终端记录.txt')
        open(f'{self.scripts_path}/Fluent终端记录.txt', 'w').close()
        self.Search_Scripts(self.scripts_path, ".log", "Fluent-", 1)  # 检索fluent脚本，并添加进数组中
        for i in range(len(self.scripts_list[1])):
            self.progress("求解计算", len(self.scripts_list[1]), i + 1)
            command = f"fluent 3d -t{self.NumCore} -g -wait -i {self.scripts_list[1][i]} &&exit" # 3ddp为双精度
            a = subprocess.Popen(command, 
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT,
                                encoding=sys.getdefaultencoding(), # 使用默认编码
                                errors='replace'  # 替换无法解码的字符
                                )  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
            terminal_record = open(f'{self.scripts_path}/Fluent终端记录.txt', 'a+', encoding='utf-8')
            while a.poll() is None:
                line = a.stdout.readline()
                self.window['state_print'].print('{:0>2d}* '.format(i + 1) + line)
                terminal_record.write(line + "\n")
            terminal_record.close()
            name = os.path.basename(self.scripts_list[1][i])
            name = name.split('.')[0]
            sg.cprint(f'已生成： {name} .dat 文件与 {name} .cas 文件')
            self.window['state_print'].print(f'已生成：{name}.dat 文件与{name}.cas 文件', text_color='red')
            self.window['state_print'].print(" ")
            
            
    

    # 批量运行CFD_Post脚本 #
    def CFD_Post(self):  # 批量进行后处理
        self.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        for i in range(len(self.scripts_list[2])):
            (filename,extension) = os.path.splitext(self.scripts_list[2][i])
            pattern_num=int(filename.split('Post-')[1])
            self.window['state_print'].print(f"********** 开始进行第{pattern_num}组后处理 **********", text_color='red')
            self.progress("Post后处理", len(self.scripts_list[2]), i+1)
            command = f"cfdpost -batch {self.scripts_list[2][i]} &&exit"
            a = subprocess.Popen(command, 
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT,
                                encoding=sys.getdefaultencoding(), # 使用默认编码
                                errors='replace'  # 替换无法解码的字符
                                )  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
            while a.poll() is None:
                line = a.stdout.readline()
                self.window['state_print'].print('{:0>2d}* '.format(pattern_num) + line)
            sg.cprint(f'已完成 {str(pattern_num)} 组后处理', text_color='red')
            self.window['state_print'].print(f'已完成 {str(pattern_num)} 组后处理', text_color='red')
            self.Revise_csv(pattern_num) # 将结果文件数据转移到实验规划表中
            self.window['state_print'].print(" ")
        

    # 即时运行CFD_Post脚本子方法 #
    def CFD_Post_Alone(self, num, all_num):
        self.window['state_print'].print("********** 开始进行第" + str(num+1) + "组后处理 **********", text_color='red')
        command = f"cfdpost -batch {self.scripts_list[2][num]} &&exit"
        a = subprocess.Popen(command, 
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT,
                                encoding=sys.getdefaultencoding(), # 使用默认编码
                                errors='replace'  # 替换无法解码的字符
                                )  # 此时打开的a是一个对象，如果直接打印的话是对象内存地址
        while a.poll() is None:
            line = a.stdout.readline()
            self.window['state_print'].print('{:0>2d}* '.format(num+1) + line)
        sg.cprint(f"********** 已完成第 {str(num+1)} 组后处理 **********", text_color='red')
        self.window['state_print'].print("{:0>2d}组数据已写入Result.csv".format(num+1), text_color='red')
        self.window['state_print'].print(" ")
        self.Revise_csv(num+1) # 将结果文件保存到实验规划表中
        self.window['state_print'].print(f"已完成： 第 {str(num+1)} 组后处理", text_color='red')
        self.window['state_print'].print(" ")
        self.window['state_print'].print("----------------------------------------------------------")
        self.window['state_print'].print(" ")
        if str(all_num) == str(num+1):
            self.window['state_print'].print('本次运行结束', text_color='red')
            sg.cprint('本次运行结束', text_color='red')

    # 即时运行CFD_Post脚本总方法 #
    def CFD_Post_Immediate(self):
        scripts_num = len(self.scripts_list[2])
        
        for j in range(len(self.scripts_list[2])):
            (filename,extension) = os.path.splitext(self.scripts_list[2][j])
            pattern_num=int(filename.split('Post-')[1]) # 从脚本路径中选出需要匹配的序号
            while True:
                pattern = re.compile("Fluent-{:0>2d}".format(pattern_num)+'.plt')
                for root, dirs, files in os.walk(self.result_path):
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

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
LastEditTime : 2023-07-11 21:20:46 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : \CFD-Automatic-Simulation-Software\main.py
Description  : 
------------------------------------------------------------------------
'''
import sys
import os
import time
import threading
import PySimpleGUI as sg


from Functional_modules.GUI import create_window
from Functional_modules.SearchRemove import SearchRemove
from Functional_modules.Prepare import Prepare
from Functional_modules.Progress import Progress
from Functional_modules.Script import Script
from Functional_modules.Calculate import Calculate
from Functional_modules.Run import Run


scripts_path = os.path.dirname(sys.argv[0]) + "\ANSYS_Python_Project\Script"  # 生成的脚本文件路径
result_path = os.path.dirname(sys.argv[0]) + "\ANSYS_Python_Project\Result"  # 网格文件路径，几何文件路径，结果文件路径

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



# 创建窗口对象
window = create_window()
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

            # 接受GUI传入的参数
            NumVarGeom = values['几何变量']
            NumVarPhy = values['物理变量']
            NumRes = values['响应数目']
            TemUnit = values['温度单位']
            TemEnv = values['环境温度']
            NumCore = values['核心数目']
            NumIter = values['迭代次数']
            PathTable = values['规划表路径']
            PathTemp = values['脚本模板路径']

            BooleRunDm = values['DM修改']
            BooleRunMesh = values['Mesh生成']
            BooleRunFluent = values['Fluent求解']
            BooleRunPost = values['Post处理']
            BooleSciptMesh = values['Mesh脚本']
            BooleSciptFluent = values['Fluent脚本']
            BooleSciptPost = values['Post脚本']

            # 初始化Prepare类
            Class_Prepare = Prepare(window, PathTable, scripts_path, result_path)  # 初始化 准备工作类
            index_all, G_name, W_name, excel_Gdata, excel_Wdata, RRS_Gdata = Class_Prepare.excel(int(NumVarGeom), int(NumVarPhy), int(NumRes))  # 读取excel获取excel数据
            Class_Prepare.create_folder()  # 创建文件夹
            Class_Prepare.create_csv()  # 创建空白结果文件

            # 初始化Progress类
            Progress(window)

            # 初始化脚本生成类
            Class_Script = Script(window,PathTemp,PathTable, scripts_path, result_path,TemUnit,TemEnv,NumIter,index_all, W_name, excel_Gdata, excel_Wdata, RRS_Gdata)  # 初始化脚本生成类
            
            # 初始化脚本计算类
            Class_Calculate = Calculate(window,PathTable, scripts_path, result_path, NumCore,NumVarGeom,NumVarPhy,NumRes,G_name,RRS_Gdata )

            # 初始化脚本运行类
            Class_Run = Run(window,int(time.time()),Class_Script,Class_Calculate, scripts_path, result_path)

            # 设置功能组合对应的条件
            conditions = {
                # 单独运行模块，同时生成脚本
                (False,False,False,True,False,False,False): Class_Run.DM,
                (True,False,False,False,True,False,False): Class_Run.Mesh,
                (False,True,False,False,False,True,False): Class_Run.Fluent,
                (False,False,True,False,False,False,True): Class_Run.Post,
                # 同时运行两个模块，并同时生成脚本
                (True,False,False,True,True,False,False): Class_Run.DM_Mesh,
                (True,True,False,False,True,True,False): Class_Run.Mesh_Fluent,
                (False,True,True,False,False,True,True): Class_Run.Fluent_Post,
                # 同时运行三个模块，并同时生成脚本
                (True,True,False,True,True,True,False): Class_Run.DM_Mesh_fluent,
                (True,True,True,False,True,True,True): Class_Run.Mesh_Fluent_Post,
                # 同时运行四个模块，并同时生成脚本
                (True,True,True,True,True,True,True): Class_Run.DM_Mesh_Fluent_Post,
                # 单独运行模块，不生成脚本
                (False,False,False,False,True,False,False): Class_Run.Only_Mesh_Run,
                (False,False,False,False,False,True,False): Class_Run.Only_Fluent_Run,
                (False,False,False,False,False,False,True): Class_Run.Only_Post_Run,
                # 同时运行两个模块，不生成脚本
                (False,False,False,False,False,True,True): Class_Run.Nos_Fluent_Post,
                # 同时运行三个模块，不生成脚本
                (False,False,False,False,True,True,True): Class_Run.Nos_Mesh_Fluent_Post,

                # 单独生成脚本
                (True,False,False,False,False,False,False): Class_Run.Mesh_Script,
                (False,True,False,False,False,False,False): Class_Run.Fluent_Script,
                (False,False,True,False,False,False,False): Class_Run.Post_Script,
            }
            # 获取输入的功能组合
            GetValue = (BooleSciptMesh, BooleSciptFluent, BooleSciptPost, BooleRunDm, BooleRunMesh, BooleRunFluent, BooleRunPost)
            # 遍历 寻找与输入功能组合对应的组合命令，并创建线程运行
            for key, value in conditions.items():
                if key == GetValue:
                    threading.Thread(target=conditions.get(key), daemon=True, ).start()
                    break
            else:
                window['state_print'].print('功能组合无效，请调整功能组合选项')

    if event == '清除':
        window['运行'].update(disabled=False, )
        window['脚本模板路径按钮'].update(disabled=False, )
        window['规划表路径按钮'].update(disabled=False, )
        try:
            SearchRemove(window,os.path.dirname(sys.argv[0]), ".trn", "任意")
            SearchRemove(window,os.path.dirname(sys.argv[0]), ".bat", "任意")
            SearchRemove(window,os.path.dirname(sys.argv[0]), ".log", "任意")
        except WindowsError:
            window['state_print'].print(f'Error： 文件被占用，清除失败！\n地址：{os.path.dirname(sys.argv[0])}\n请解除！', text_color='red')

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
# 尝试解决Fluent 2023R1 打印不出控制台信息的问题 主要修改subprocess.Popen命令，修改失败

# 2023/7/11 12:30
# 解决了Fluent 2023R1 打印不出控制台信息的问题 原因是subprocess.Popen实时打印的问题，具体来说应该是编码问题
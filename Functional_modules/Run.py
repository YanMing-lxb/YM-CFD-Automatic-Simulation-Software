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
LastEditTime : 2024-07-30 15:13:59 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /YM-CFD-Automatic-Simulation-Software/Functional_modules/Run.py
Description  : 
 -----------------------------------------------------------------------
'''

import time
import threading
import PySimpleGUI as sg

from Functional_modules.SearchRemove import SearchRemove

class Run(object):
    def __init__(self,window, time_start,Class_Script,Class_Calculate, scripts_output_path, result_output_path):
        self.window = window
        self.time_start = int(time_start)
        self.Class_Script=Class_Script
        self.Class_Calculate=Class_Calculate
        self.scripts_path = scripts_output_path
        self.result_path = result_output_path
        self.time_stop = False

    #  更新时间
    def update_time(self):
        while True:
            time_end = int(time.time())
            time_run = time_end - int(self.time_start)
            self.window['运行时间'].update(
                value=str((time_run // 60 // 60)) + "小时 " + str(int(time_run // 60 % 60)) + "分钟 " + str(
                    round(time_run % 60)) + "秒")
            time.sleep(0.2)
            if self.time_stop is True:
                break
    def DM(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.result_path, ".agdb", "Geom")
        self.Class_Calculate.DM()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Mesh(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        self.Class_Script.Fluent_Meshing()
        self.Class_Calculate.Fluent_Meshing()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        self.Class_Script.Fluent()
        self.Class_Calculate.Fluent()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".cse", "CFD_Post")
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        self.Class_Script.CFD_Post()
        self.Class_Calculate.CFD_Post()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def DM_Mesh(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        SearchRemove(self.window,self.result_path, ".agdb", "Geom")
        self.Class_Calculate.DM()
        self.Class_Script.Fluent_Meshing()
        self.Class_Calculate.Fluent_Meshing()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')


    def Mesh_Fluent(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        self.Class_Script.Fluent_Meshing()
        self.Class_Script.Fluent()
        self.Class_Calculate.Fluent_Meshing()
        self.Class_Calculate.Fluent()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent_Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        SearchRemove(self.window,self.scripts_path, ".cse", "CFD_Post")
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        self.Class_Script.Fluent()
        self.Class_Script.CFD_Post()
        self.Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=self.Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        self.Class_Calculate.Fluent()
        self.time_stop = True

    def DM_Mesh_fluent(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        SearchRemove(self.window,self.result_path, ".agdb", "Geom")
        self.Class_Calculate.DM()
        self.Class_Script.Fluent_Meshing()
        self.Class_Script.Fluent()
        self.Class_Calculate.Fluent_Meshing()
        self.Class_Calculate.Fluent()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Mesh_Fluent_Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        SearchRemove(self.window,self.scripts_path, ".cse", "CFD_Post")
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        self.Class_Script.Fluent_Meshing()
        self.Class_Script.Fluent()
        self.Class_Script.CFD_Post()
        self.Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=self.Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        self.Class_Calculate.Fluent_Meshing()
        self.Class_Calculate.Fluent()
        self.time_stop = True


    def DM_Mesh_Fluent_Post(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        SearchRemove(self.window,self.scripts_path, ".cse", "CFD_Post")
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        SearchRemove(self.window,self.result_path, ".agdb", "Geom")
        self.Class_Calculate.DM()
        self.Class_Script.Fluent_Meshing()
        self.Class_Script.Fluent()
        self.Class_Script.CFD_Post()
        self.Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=self.Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        self.Class_Calculate.Fluent_Meshing()
        self.Class_Calculate.Fluent()
        self.time_stop = True


        

    def Only_Mesh_Run(self): # 不生成脚本文件，使用已有的脚本
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        self.Class_Calculate.Fluent_Meshing()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Only_Fluent_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        self.Class_Calculate.Fluent()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Only_Post_Run(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        self.Class_Calculate.CFD_Post()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')




    def Nos_Fluent_Post(self):  # 直接使用已生成的脚本
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        self.Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=self.Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        self.Class_Calculate.Fluent()
        self.time_stop = True

    def Nos_Mesh_Fluent_Post(self):  # 直接使用已生成的脚本
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.result_path, ".msh", "Mesh")
        SearchRemove(self.window,self.result_path, ".cas", "Fluent")
        SearchRemove(self.window,self.result_path, ".dat", "Fluent")
        SearchRemove(self.window,self.result_path, ".plt", "Fluent")
        SearchRemove(self.window,self.result_path, ".png", "CFD_Post")
        self.Class_Calculate.Search_Scripts(self.scripts_path, ".cse", "CFD_Post-", 2)  # 检索cfd_post脚本，并添加进数组中
        threading.Thread(target=self.Class_Calculate.CFD_Post_Immediate, daemon=True, ).start()
        self.Class_Calculate.Fluent_Meshing()
        self.Class_Calculate.Fluent()
        self.time_stop = True



    def Mesh_Script(self): # 只生成脚本文件
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Mesh")
        self.Class_Script.Fluent_Meshing()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Fluent_Script(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".log", "Fluent")
        self.Class_Script.Fluent()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')

    def Post_Script(self):
        threading.Thread(target=self.update_time, daemon=True, ).start()
        SearchRemove(self.window,self.scripts_path, ".cse", "CFD_Post")
        self.Class_Script.CFD_Post()
        self.time_stop = True
        self.window['state_print'].print('本次运行结束', text_color='red')
        sg.cprint('本次运行结束', text_color='red')






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
LastEditTime : 2024-07-30 15:14:09 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /YM-CFD-Automatic-Simulation-Software/Functional_modules/Script.py
Description  : 
 -----------------------------------------------------------------------
'''

#  创建脚本文件
class Script(Progress):
    def __init__(self, window, PathTemp,PathTable, Script_Output_Path, Result_Path,TemUnit,TemEnv,NumIter,index_all, W_name, excel_Gdata, excel_Wdata, RRS_Gdata):
        self.window =window
        self.PathTemp = PathTemp
        self.PathTable =PathTable
        self.Script_Output_Path = Script_Output_Path
        self.Result_Path = Result_Path
        self.TemUnit = TemUnit
        self.TemEnv = TemEnv
        self.NumIter = NumIter
        self.index_all = index_all
        self.W_name=W_name
        self.excel_Gdata=excel_Gdata
        self.excel_Wdata=excel_Wdata
        self.RRS_Gdata =RRS_Gdata

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
                    line = line.replace("温度单位", self.TemUnit.lower())
                if "环境温度" in line:
                    if self.TemUnit == 'K':
                        line = line.replace("环境温度", str(float(self.TemEnv) + 273.15))
                    else:
                        line = line.replace("环境温度", self.TemEnv)
                if "迭代次数" in line:
                    line = line.replace("迭代次数", self.NumIter)
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
                    line = line.replace("温度单位", self.TemUnit)
                if "结果文件路径" in line:
                    line = line.replace("结果文件路径", f'{os.path.dirname(self.PathTable)}/Result.csv')
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
        self.window['state_print'].print("已生成： " + output_name + suffix + " 文件", text_color='red')

    #  创建Fluent_Meshing脚本
    def Fluent_Meshing(self):  # 模板脚本的输入路径，模板脚本输出路径
        if self.RRS_Gdata[0]: # 判断数组是否为空，也就是是否有几何变量。
            for i in range(len(self.RRS_Gdata)):
                input_name = "Geom-" + '-'.join(self.RRS_Gdata[i])
                output_name = "Mesh-" + '-'.join(self.RRS_Gdata[i])
                self.Replacement_module(self.PathTemp + "/fluent_meshing.txt",self.Script_Output_Path, input_name, output_name, None, None, ".agdb",".msh", ".log", None, 'fluent_meshing')
                self.progress("网格脚本", len(self.RRS_Gdata), i+1)

        elif not self.RRS_Gdata[0]: # 如果几何变量为空，执行下一步
            input_name = "Geom"
            output_name = "Mesh"
            self.Replacement_module(self.PathTemp + "/fluent_meshing.txt", self.Script_Output_Path,input_name, output_name, None, None, ".agdb", ".msh", ".log", None,'fluent_meshing')
            self.progress("网格脚本", 1, 1)


    #  创建Fluent脚本
    def Fluent(self):  # 模板脚本的输入路径，模板脚本输出路径
        for i in range(len(self.index_all)):
            if self.RRS_Gdata[0] and self.excel_Wdata[0]:
                replace_list=self.excel_Wdata[i]
                input_name = "Mesh-" + '-'.join(self.excel_Gdata[i])
                output_name = "Fluent-{:0>2d}".format(int(self.index_all[i]))
                self.Replacement_module(self.PathTemp + "/fluent.txt", self.Script_Output_Path,input_name, output_name, self.W_name, replace_list, ".msh", "", ".log", None,"fluent")
                self.progress("Fluent脚本", len(self.index_all), i + 1)
            elif not self.RRS_Gdata[0] and self.excel_Wdata[0]:
                replace_list = self.excel_Wdata[i]
                input_name = "Mesh"
                output_name = "Fluent-{:0>2d}".format(int(self.index_all[i]))
                self.Replacement_module(self.PathTemp + "/fluent.txt",self.Script_Output_Path, input_name, output_name,self.W_name, replace_list, ".msh", "", ".log", None, "fluent")
                self.progress("Fluent脚本", len(self.index_all), i + 1)

            elif self.RRS_Gdata[0] and not self.excel_Wdata[0]:
                input_name = "Mesh-" + '-'.join(self.excel_Gdata[i])
                output_name = "Fluent-{:0>2d}".format(int(self.index_all[i]))
                self.Replacement_module(self.PathTemp + "/fluent.txt", self.Script_Output_Path,input_name, output_name, self.W_name, None, ".msh", "", ".log", None, "fluent")
                self.progress("Fluent脚本", len(self.index_all), i + 1)
            else:
                self.window['state_print'].print("变量必须存在，请重新输入！", text_color='red')


    #  创建CFD_Post脚本
    def CFD_Post(self):
        for i in range(len(self.index_all)):
            input_name = "Fluent-{:0>2d}".format(int(self.index_all[i]))
            output_name = "CFD_Post-{:0>2d}".format(int(self.index_all[i]))
            self.Replacement_module(self.PathTemp + "/cfd_post.cse", self.Script_Output_Path,
                                    input_name, output_name, None, None, ".dat", "-", ".cse", str(i + 2), "cfd_post")
            self.progress("后处理脚本", len(self.index_all), i + 1)
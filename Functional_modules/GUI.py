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
Date         : 2023-07-11 13:03:38 +0800
LastEditTime : 2023-07-11 14:50:53 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : \CFD-Automatic-Simulation-Software\GUI.py
Description  : 
 -----------------------------------------------------------------------
'''

import os
import sys
import PySimpleGUI as sg

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

def create_window():
    # 配置窗口布局

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

    return window
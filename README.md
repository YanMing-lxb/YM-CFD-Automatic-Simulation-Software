<!--
 *  =======================================================================
 *  ····Y88b···d88P················888b·····d888·d8b·······················
 *  ·····Y88b·d88P·················8888b···d8888·Y8P·······················
 *  ······Y88o88P··················88888b·d88888···························
 *  ·······Y888P··8888b···88888b···888Y88888P888·888·88888b·····d88b·······
 *  ········888······"88b·888·"88b·888·Y888P·888·888·888·"88b·d88P"88b·····
 *  ········888···d888888·888··888·888··Y8P··888·888·888··888·888··888·····
 *  ········888··888··888·888··888·888···"···888·888·888··888·Y88b·888·····
 *  ········888··"Y888888·888··888·888·······888·888·888··888··"Y88888·····
 *  ·······························································888·····
 *  ··························································Y8b·d88P·····
 *  ···························································"Y88P"······
 *  =======================================================================
 * 
 * Author       : 焱铭
 * Date         : 2023-07-04 12:14:38 +0800
 * LastEditTime : 2023-07-04 13:15:55 +0800
 * Github       : https://github.com/YanMing-lxb/
 * FilePath     : \YM-CFD-Automatic-Simulation-Software\README.md
 * Description  : 
 * ------------------------------------------------------------------------
 -->

# YM-CFD-Automatic-Simulation-Software
[![](https://img.shields.io/github/issues/YanMing-lxb/YM-CFD-Automatic-Simulation-Software)](https://github.com/YanMing-lxb/YM-CFD-Automatic-Simulation-Software/issues)  ![Downloads latest release](https://img.shields.io/github/downloads/YanMing-lxb/YM-CFD-Automatic-Simulation-Software/latest/total?color=blueviolet)

***点个⭐支持一下！***
## 使用前提
本软件的原理是依照EXCEL中的实验规划表对Fluent Meshing、Fluent、CFD Post的脚本进行修改，并依次运行脚本以达到自动仿真的效果，因此在使用该软件之前需要注意下面两点。

### 配置环境变量
该软件基于ANSYS Workben开发，因此在使用该软件之前需要对配置几个环境变量。

在系统变量的Path变量下配置以下路径：

以ANSYS 2020 R2 为例：
1. D:\Application\ANSYS Inc\v202\Framework\bin\Win64\runwb2.exe
2. D:\Application\ANSYS Inc\v202\CFD-Post\bin
3. D:\Application\ANSYS Inc\v202\fluent\ntbin\win64
其中`D:\Application`为ANSYS安装路径，请根据自己的安装位置自行更换。

### 脚本基础
根据该软件的原理可以知道，使用该软件的前提是掌握脚本的编写：
1. Fluent Meshing与Fluent的脚本均为TUI命令编写，关于TUI命令的说明文档可在Fluent中的`Help`  ⇒ `User's Guide Contents`⇒ `III. Solution Mode `⇒`2. Text User Interface (TUI) `⇒`Fluent Text Command List `中找到(如英语不好也可使用翻译软件通过翻译页面进行阅读)；
2. CFD Post提供脚本录制功能，请自行搜索如何录制CFD Post的脚本；

本项目提供用于稳态共轭传热的Fluent Meshing、Fluent、CFD Post脚本[**模板示例**](https://github.com/YanMing-lxb/YM-CFD-Automatic-Simulation-Software/tree/main/Script_template)；

> ps: 作者在使用该软件时，CFD Post仅作为数据提取工具，等值线图、流线图均采用Tecplot 360绘制(该用法仅供参考！)


## 使用说明
在使用本程序之前需注意以下几点：

1. 定义：
    - 几何变量：改变几何的变量
    - 物理变量：其他改变物理参数的变量，如流速、温度、材料参数等；物理变量为直接输入脚本中的数据，如有类似纳米流体体积分数这种需要换算成特定体积分数的纳米流体物性参数的，如将体积分数换算成密度、比热容、导热率、粘度的，则物理变量数目按照换算后的个数来计算，即体积分数占4个物理变量。
    - 响应数目：应得到的响应的数目
    - 环境温度：初始化时所有部件的温度。
2. 实验规划表为excel文件，需放在.xls后缀的excel文件中，注意第一列为序号、几何变量需放在前几列、后面为物理变量、最后为响应值；
3. 使用本软件之前需制作脚本模板。本程序修改模板原理是寻找关键词，替换为实验规划表中对应变量，因此脚本模板中除几个特殊的关键词其他关键词需与实验规划表中变量名称一致。
4. 特殊关键词：如inlet温度与环境温度相同，可以将inlet温度替换为关键字：
环境温度
    - fluent中：输入、输出、温度单位、迭代次数、环境温度
    - fluent_meshing中：输入、输出
    - cfd_post中：输入、输出、温度单位、序号、结果文件路径
5. 模板脚本名称为固定名称分别为：fluent.txt（utf-8）、fluent_meshing.txt（utf-8）、cfd_post.cse（ansi）（可以文本文档打开编辑）
>ps: 要求cfd_post.cse文件为cfd_post生成的文件否则会出现编码错误(可在[**模板示例**](https://github.com/YanMing-lxb/YM-CFD-Automatic-Simulation-Software/tree/main/Script_template)的基础上改)。
6. 几何模型无法自动生成，因此需要DM导出的几何模型其后缀为.agdb。
7. 文件命名规则：
    - 几何模型：Geom-几何变量1-几何变量2.agdb,依次往下类推（如：当几何变量中的布局为1，当量直径为0.5，特征长度为7，此时几何模型命名应为：Geom-1-0.5-7.agdb）
    - 网格文件：命名规则与几何模型相同，Mesh-几何变量1-几何变量2.msh依次往下类推
    - fluent结果文件自动生成，无需注意。

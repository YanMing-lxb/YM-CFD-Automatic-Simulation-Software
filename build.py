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
LastEditTime : 2024-07-30 19:39:56 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /YM-CFD-Automatic-Simulation-Software/build.py
Description  : 
 -----------------------------------------------------------------------
'''

from PyInstaller.__main__ import run
import shutil
import os

def check_and_create_folder():
    root_dir = os.getcwd()  # 获取当前工作目录
    releases_dir = os.path.join(root_dir, "Releases")

    if not os.path.exists(releases_dir):
        os.makedirs(releases_dir)
        print("成功创建 Releases 文件夹")
    else:
        print("Releases 文件夹已存在")

def del_file(file):
    # 检查文件是否存在
    if os.path.exists(file):
        # 删除文件
        os.remove(file)
        print(f"{file}删除成功！")
    else:
        print(f"{file}不存在！")

def move_file(res_folder, file_name, des_folder):
    res_file_path = os.path.join(res_folder, file_name +'.exe')  # 源文件路径
    des_file_path = os.path.join(des_folder, file_name+'.exe')  # 目标文件路径

    # 移动文件
    shutil.move(res_file_path, des_file_path)
    print(f"已将文件 {file_name}.exe 从{res_folder}移动到 {des_folder} 文件夹。")


def build_pyinstaller(exe_name, resource, icon_pic):
    args1 = [
        'main.py',  # 要打包的主程序文件
        '-w',  # 指定为窗口应用程序（无命令行界面）
        f'--icon={resource}/{icon_pic}',  # 设置主窗口的图标路径，使用 icon_pic 参数作为图标文件
        f'--add-data={resource};{resource}',  # 将 Resource_files 文件夹中的所有文件添加到可执行文件中
        '--onefile',  # 生成单个可执行文件
        '--clean',
        f'--name={exe_name}'  # 指定可执行文件的名称，使用 exe_name 参数作为可执行文件名
    ]

    args2 = [
        exe_name+".spec"
    ]

    run(args1)
    run(args2)


if __name__ == '__main__':
    # 设置参数
    version = 'v4.2.0' # 软件版本
    file_name = f'CFD Automatic Simulation Software {version} by YanMing'  # 可执行文件名
    resource = "CASS-Resource" # 资源文件夹名
    icon_pic = 'CASS-logo.ico'  # 图标文件名
    des_folder = 'Releases'  # 将生成的exe移动到的目标文件夹名
     
    check_and_create_folder() # 检查是否存在“Releases”文件夹，没有就创建
     
    build_pyinstaller(file_name, resource, icon_pic)  # 调用方法编译生成可执行文件
 
    move_file('dist', file_name, des_folder)  # 移动文件到目标文件夹
 
    # 删除不需要的文件和文件夹
    shutil.rmtree('dist')  # 删除 dist 文件夹
    shutil.rmtree('build')  # 删除 build 文件夹
    del_file(f"{file_name}.spec")  # 删除 .spec 文件
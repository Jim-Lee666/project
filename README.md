import subprocess
import os


def load_file():
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # config.ini文件路径,获取当前目录的父目录的父目录与congig.ini拼接
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."), 'config.ini')
    print('当前目录:' + current_path)
    print('当前父目录:' + father_path)
    print('config.ini路径:' + config_file_path)


load_file()


def cmd(command):
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    subp.wait(2)
    if subp.poll() == 0:
        print(subp.communicate()[1])
    else:
        print("失败")


# LINBIT
#cmd("journalctl -u linstor-controller | cat")  # 查看日志命令
#cmd("journalctl -u linstor-controller --since '2021-06-10' --until '2021-06-22 03:00' | cat ")  # 指定时间查看
#cmd("journalctl -u linstor-controller | cat > linstor-controller.log")  # 将日志保存至指定文件


# DRBD
#cmd("dmesg -T | grep drbd")  # 日志查看
#cmd("dmesg -T | grep drbd | cat > drbd.log")  # 将日志保存至指定文件




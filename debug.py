# -*- coding:utf-8 -*-

import subprocess
import os
import time
import paramiko
import yaml


def exec_cmd(command,ssh_obj=None):
    if ssh_obj:
        result = ssh_obj.exec_cmd(command)
    else:
        result = subprocess.run(command, shell=True)
    print(result)


# LINBIT
# cmd("journalctl -u linstor-controller | cat")  # 查看日志命令
# cmd("journalctl -u linstor-controller --since '2021-06-10' --until '2021-06-22 03:00' | cat ")  # 指定时间查看
# cmd("journalctl -u linstor-controller | cat > linstor-controller.log")  # 将日志保存至指定文件


# DRBD
# cmd("dmesg -T | grep drbd")  # 日志查看
# cmd("dmesg -T | grep drbd | cat > drbd.log")  # 将日志保存至指定文件


# CRM
# cat /var/log/pacemaker.log  #查看pacemaker日志命令
# crm_report --from	"$(date	-d "7 days ago" +"%Y-%m-%d	%H:%M:%S")"	/tmp/crm_report_${HOSTNAME}_$(date +"%Y-%m-%d")
# 收集crm_report命令
# tar -jxvf file_name #解压


def save_linbit_file(path,ssh_obj=None):
    cmd = f'journalctl -u linstor-controller | cat > {path}/linstor-controller.log'
    exec_cmd(cmd,ssh_obj)


def save_drbd_file(path,ssh_obj=None):
    cmd = f'dmesg -T | grep	drbd | cat > {path}/drbd.log'
    exec_cmd(cmd,ssh_obj)


def save_crm_file(path,ssh_obj=None):
    cmd = f'crm_report --from "$(date -d "7 days ago" +"%Y-%m-%d %H:%M:%S")" {path}/crm.log'
    exec_cmd(cmd,ssh_obj)


def get_path(soft):
    log_path = '/home/'
    node = 'samba/'
    path = f'{log_path}/{node}/{soft}/{time.strftime("%Y%m%d_%H%M%S")}/'
    return path


def mkdir(path):
    cmd = f"mkdir -p {path}"
    exec_cmd(cmd)


class SSHConn(object):

    def __init__(self, host, port=22, username=None, password=None, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._username = username
        self._password = password
        self.SSHConnection = None
        self.ssh_connect()

    def _connect(self):
        try:
            objSSHClient = paramiko.SSHClient()    # 创建SSH对象
            objSSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接其他主机
            objSSHClient.connect(self._host, port=self._port,
                                 username=self._username,
                                 password=self._password,
                                 timeout=self._timeout)  # 连接服务器
            # time.sleep(1)
            # objSSHClient.exec_command("\x003")
            self.SSHConnection = objSSHClient
        except:
            pass

    def ssh_connect(self):
        self._connect()
        if not self.SSHConnection:
            print('Connect retry for SAN switch "%s" ...' % self._host)
            self._connect()

    def exec_cmd(self, command):
        if self.SSHConnection:
            stdin, stdout, stderr = self.SSHConnection.exec_command(command)
            data = stdout.read()
            if len(data) > 0:
                # print(data.strip())
                return data
            err = stderr.read()
            if len(err) > 0:
                # 记录一下log
                pass
            #     print('''Excute command "{}" failed on "{}" with error:
            # "{}"'''.format(command, self._host, err.strip()))


class ConfFile():
    def __init__(self):
        self.yaml_file = './config.yaml'
        self.cluster = self.read_yaml()

    def read_yaml(self):
        """读YAML文件"""
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                yaml_dict = yaml.safe_load(f)
            return yaml_dict
        except FileNotFoundError:
            print("Please check the file name:", self.yaml_file)
        except TypeError:
            print("Error in the type of file name.")

    def update_yaml(self):
        """更新文件内容"""
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.cluster, f, default_flow_style=False)

    def get_ssh_conn_data(self):
        lst = []
        for node in self.cluster['node']:
            lst.append([node['public_ip'], node['port'], 'root', node['root_password']])
        return lst

    



if __name__ == "__main__":
    linbit_path = get_path('LINBIT')
    drbd_path = get_path('DRBD')
    crm_path = get_path('CRM')
    mkdir(linbit_path)
    mkdir(drbd_path)
    mkdir(crm_path)
    save_linbit_file(linbit_path)
    save_drbd_file(drbd_path)
    save_crm_file(crm_path)

    # ssh_obj = SSHConn("10.203.1.185",22,'root','password')
    # result = ssh_obj.exec_cmd("cd /home/samba && ls")
    # print(result)

    # 实例化配置文件对象
    conf_obj = ConfFile()

    # 获取要用来连接的ssh数据
    list_ssh_data = conf_obj.get_ssh_conn_data()


    # 取出数据
    for ssh in list_ssh_data:
        # ssh[0]  IP
        # ssh[1] 22
        # ssh[2] hostname
        # ssh[3] password

        # 进行ssh连接（实例化ssh对象）
        ssh_obj = SSHConn(ssh[0],ssh[1],ssh[2],ssh[3])
        # ssh对象拥有exec_cmd的方法，即在连接过去的主机去执行命令
        print(ssh_obj.exec_cmd('pwd'))


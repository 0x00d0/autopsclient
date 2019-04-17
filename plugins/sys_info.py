#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import psutil
import urllib.request
import docker
import os
import platform


from conf import settings


def get_os_info():
    '''
    获取操作系统信息
    '''

    release = subprocess.Popen("lsb_release -a | grep 'Description'", stdout=subprocess.PIPE, shell=True)
    release = release.stdout.read().decode().split(":")
    kernel_version = subprocess.Popen('uname -r', stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    architecture = subprocess.Popen('uname -p', stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    systemtime = subprocess.Popen('date', stdout=subprocess.PIPE, shell=True).stdout.read().decode()

    data_dic = {
        "os_release": release[1].strip() if len(release) > 1 else "",
        'kernel_version': kernel_version,
        'architecture': architecture,
        'systemtime': systemtime,
    }

    return data_dic


def get_cpu_info():
    cpu_count = psutil.cpu_count()  # 获取CPU逻辑个数
    cpu_core_count = psutil.cpu_count(logical=False)  # 获取CPU物理个数
    cpu_dict = {
        'cput_count': cpu_count,
        'cpu_core_count': cpu_core_count
    }

    return cpu_dict


def get_mem_info():
    swap_memory = psutil.swap_memory()  # 获取swap分区信息
    total_memory = psutil.virtual_memory().total  # 获取内存总数

    return total_memory


def get_disk_info():
    disk_key = {}
    disk_list = []
    for partitions in psutil.disk_partitions():
        # disk_key[partitions[0]] = {partitions[1]:partitions[2]}
        disk_usage = psutil.disk_usage(partitions[1])
        # print('disk_usage',disk_usage[0])
        # disk_key[partitions[0]] = [{partitions[1]:disk_usage[0]/1024/1024},{'fstype':partitions[2]}]
        disk_key[partitions[0]] = {partitions[1]: disk_usage[0] / 1024 / 1024, 'fstype': partitions[2]}
        disk_list.append({partitions[0]: {partitions[1]: disk_usage[0] / 1024 / 1024, 'fstype': partitions[2]}})

    return disk_list


def get_docker_info():
    client = docker.from_env()
    docker_info = client.info()

    docker_version = docker_info.get('ServerVersion')  # ServerVersion
    storage_driver = docker_info.get('Driver')  # 存储驱动
    containers = docker_info.get('Containers')  # 容器数量
    containers_running = docker_info.get('ContainersRunning')  # 运行容器数量
    containers_paused = docker_info.get('ContainersPaused')  # 暂停运行的容器数量
    containers_stopped = docker_info.get('ContainersStopped')  # 停止运行的容器数量
    containers_images = docker_info.get('Images')  # 容器镜像数量

    docker_info_dict = {

        'storage_driver': storage_driver,
        'containers': containers,
        'containers_running': containers_running,
        'containers_paused': containers_paused,
        'containers_stopped': containers_stopped,
        'containers_images': containers_images,
        'docker_version': docker_version,
        'containers_list': [],
    }
    containers_id_str = subprocess.Popen("docker ps -a | grep -v 'COMMAND' | awk ' { print $1 } '",
                                         stdout=subprocess.PIPE, shell=True).stdout.read().decode()

    if containers_id_str:
        containers_id_list = containers_id_str.split('\n')
        for containers_id in containers_id_list:
            if containers_id:
                container = client.containers.get(containers_id)
                if container.attrs.get('Id') not in docker_info_dict:
                    docker_info_dict.get('containers_list').append({container.attrs.get('Id'): {
                        'Image': container.attrs.get('Config').get('Image'),
                        'Env': container.attrs.get('Config').get('Env'),
                        'WorkingDir': container.attrs.get('Config').get('WorkingDir'),
                        'Platform': container.attrs.get('Platform'), 'Created': container.attrs.get('Created'),
                        'State': {'StartedAt': container.attrs.get('State').get('StartedAt'),
                                  'Status': container.attrs.get('State').get('Status')},
                        'Network': container.attrs.get('NetworkSettings').get('Networks').keys(),
                        'Ports': container.attrs.get('NetworkSettings').get('Ports'),
                        'Name': container.attrs.get('Name'),
                        'mounts': {mountskeys.get('Destination'): mountskeys.get('Source') for mountskeys in
                                   container.attrs.get('Mounts')}}})

    return docker_info_dict


def check_platform():
    result = subprocess.Popen("cat /etc/issue | awk 'NR==1{print $1}'", stdout=subprocess.PIPE,
                              shell=True).stdout.read().decode()
    if result in ['Ubuntu', 'Ubuntu\n']:
        #
        pass
    elif result in ['CentOS', 'CentOS\n']:
        subprocess.Popen("yum install -y redhat-lsb", stdout=subprocess.PIPE, shell=True).stdout.read().decode()


def packge_check():
    pass


def collect():
    data = dict()
    try:

        data['os_info'] = get_os_info()
        data['cpu_info'] = get_cpu_info()
        data['disk_info'] = get_disk_info()
        data['docker_info'] = get_docker_info()

    except Exception as e:
        settings.logging.error(e)
        print(e)

    return data


if __name__ == "__main__":
    data = dict()
    data['os_info'] = get_os_info()
    data['cpu_info'] = get_cpu_info()
    data['disk_info'] = get_disk_info()
    data['docker_info'] = get_docker_info()
    print(data)
    # check_platform()



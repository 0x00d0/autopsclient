# autopsclient


# 安装依赖
```
pip3 install docker==3.7.0 
yum -y install dmidecode
```

# 修改配置文件

```
cd autopsclient/conf/
vim settings.py

Params = {

    "server": "autops服务端地址",
    "port": autops服务端端口,
    "url": "/assets/report/",
    "request_timeout": 30,

}

```

# 启动

```
cd autopsclient/bin
python3 main.py
```


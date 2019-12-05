# OUC-WiFi 自动登录

## Introduction

支持 OUC-WIFI，OUC-AUTO 和办公区有线网络。  
第一次运行需要输入账号密码，将会保存在 `config.json` 中。  
注：代码经过长期打补丁，very ugly， don't read it.  

## Requirements

	requests

## Usage

```shell
python OUC-WiFi.py
python OUC-WiFi.py --once
```

## Android

### 下载安装 QPython 解释器

<a href='https://play.google.com/store/apps/details?id=org.qpython.qpy&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img alt='下载应用，请到 Google Play' src='https://play.google.com/intl/en_us/badges/images/generic/zh-cn_badge_web_generic.png' style="height:4em" height="70px" /></a>  

通过 Google Play，官网 [http://www.qpython.com/](http://www.qpython.com/)，或者 [GitHub releases](https://github.com/qpython-android/qpython/releases)。  

运行 `QPython`，自动创建目录 `/sdcard/qpython/`。  

安装依赖库 `requests`：`QPYPI`->`工具`->`QPYPI客户端`，运行：  

```shell
pip install --upgrade requests
```

### 下载脚本  

[OUC-WiFi.py](OUC-WiFi.py)  

文件移动到 /sdcard/qpython/scripts  

### QPython 程序列表  

找到 `OUC-WiFi.py`。点击运行，在后台运行此控制台。长按发送到桌面。

## Windows  

### 下载并安装 Python for Windows

官网 [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)  

下载最新版 Python 2。  
安装依赖库：  

```shell
pip install --upgrade requests
```

### 下载脚本  

[OUC-WiFi.py](OUC-WiFi.py)  

### 双击 OUC-WiFi.py 脚本运行  

建议发送到桌面

## Linux/macOS  

You are a pro, you know what to do.  

```shell
git clone https://github.com/Phuker/OUC-WiFi.git
pip install --upgrade -r requirements.txt
python OUC-WiFi.py
python OUC-WiFi.py --once
```

## docker

This service will always restart unless stopped. Edit `docker-compose.yml` to change this behavior.

```shell
git clone https://github.com/Phuker/OUC-WiFi.git
pip install --upgrade -r requirements.txt
python OUC-WiFi.py --once    # To create config.json
docker-compose up -d
```

## FAQ

## License

this repo is licensed under the **GNU General Public License v3.0**

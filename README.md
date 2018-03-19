# CAS Point System
1. 这个小项目是 CAS 小组的组内积分系统，实现的功能比较简单，适合入门学习。
2. 用到的技术主要有 Python、Flask、Jquery、BootStrap、MySQL、AJAX、JSON。
3. 小项目部署采用的结构为 Flask + uWSGI + Nginx。
4. 服务器系统为 Ubuntu 16.04。
5. Python 版本为 Python2.7。
6. 直接用了阿里云服务器的 root 用户进行部署。
7. 部署参考资料：[阿里云部署 Flask + uWSGI + Nginx 详解](http://www.cnblogs.com/Ray-liang/p/4173923.html)
8. 关于 Flask + uWSGI + Nginx 的原理性介绍请参考：[链接](https://www.cnblogs.com/Xjng/p/aa4dd23918359c6414d54e4b972e9081.html)

### 部署
#### Python 环境安装
Ubuntu16.04 默认已经安装了 Python 环境。

#### pip 工具
pip 工具是用来安装 python 包的。
```
sudo apt install pip
```

#### VirtualEnv 运行环境介绍
不同的项目可能会引用各种不同的依赖包，为了避免版本与和应用之间的冲突而造成的“依赖地狱“，VirtualEnv 就是 Python 项目中的必须品了。VirtualEnv 可以为每个Python应用创建独立的开发环境，使他们互不影响。VirtualEnv 可以做到以下三点：
1. 在没有权限的情况下安装包
2. 不同的应用可以使用不同的包
3. 包升级不影响其他应用

#### 安装 VirtualEvn
```
sudo pip install virtualenv
```

#### 创建虚拟运行环境
首先切到项目根目录下，然后执行命令 `virtualenv --no-site-packages --python=python2.7 venv`，这样就会在项目目录下创建一个新的 venv 目录。里面就是运行虚拟环境所需要的一些命令还有一些依赖包。`--no-site-packages` 参数指定已经安装到系统Python环境中的所有第三方包都不会复制过来,`--python=python2.7` 参数则指定了 python 的版本。接下来就是启用该环境，使用当前命令行状态进入虚拟环境，进入虚拟环境后，再安装 Python 包，则会将包装在虚拟环境内，而不会影响到全局的 Python 环境。

#### 进入、退出虚拟运行环境
执行命令 `source venv/bin/activate` 进入虚拟运行环境。进入后可以看到命令符前出现“(venv)”的字样。执行命令 `deactivate` 可以退出虚拟环境。


#### 安装 uWSGI
Flask 的实际生产运行环境选择并不多，比较成熟的是 Gunicorn 和 uWSGI，这里我用的是 uWSGI。
```
// 进入虚拟环境
source venv/bin/activate

// 安装 uWSGI
pip install uwsgi
```

#### 安装 Flask
这里使用清单文件一次性安装 Flask 和他的相关依赖包。清单文件名为 requirements.txt，内容如下：
```
PyMySQL==0.7.11
Flask==0.12.2
Flask_Script==2.0.6
```
安装方法如下：
``` shell
// 进入虚拟环境，然后执行以下命令
pip install -r requirements.txt
```

#### 数据库安装
由于该项目采用的是MySQL，所以需要安装以下 MySQL，安装 MySQL 不属于这个小项目讨论的重点，也比较简单，就不再赘述了。

#### 创建数据库
进入 MySQL 客户端，执行以下命令，创建该项目所需要的数据库。
``` sql
CREATE DATABASE score;
```

#### 小项目结构介绍
这里不展开介绍项目的具体目录结构，而从最上层简要介绍，我的 Flask 项目，app 是被做在包内的，在包外采用 Flask Script 写一个 manage.py 作为启动文件。
```
flask-point-system
├── app                   // Flask 程序目录
├── manange.py           // 启动文件
```

#### 启动文件介绍
这里启动文件提供了两条指令，分别是 `deploy` 和 `run`，执行方法如下：
```
python manage.py deploy  // 创建表等
python manage.py run  // 运行 app
```
这里我们先执行一下 `python manage.py deploy` 就可以了。

#### 配置 uWSGI
在项目目录下创建了一个 uwsgi-config.ini 文件。文件内容如下：
```
[uwsgi]

# uwsgi 启动时所使用的地址与端口号
socket = 127.0.0.1:8001

# 指向的网站目录
chdir =  /var/www/flask-point-system/

# python 启动程序文件
wsgi-file = manage.py

# python 程序内用以启动的 application 变量名
# callable=app 这个 app 是 manage.py 程序文件内的一个变量，这个变量的类型是 Flask的 application 类 
callable = app

# 处理器数，可以自己调整
processes = 1

# 线程数，可以自己调整
threads = 1

# 状态检测地址
stats = 127.0.0.1:9191
```
执行命令 `uwsgi uwsgi-config.ini` 来启动 uWSGI。


#### 安装配置 Supervisor
可以同时启动多个应用，最重要的是，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。Supervisor 的全局配置文件的位置是 **/etc/supervisor/supervisor.conf**，正常情况下我们并不需要去对这个全局配置文件作出任何的改动，只需要添加一个新的 *.conf 文件放在 **/etc/supervisor/conf.d/** 目录下。这里我们给出的配置文件名称为 my_flask_supervisor.conf，内容如下：
```
[program:my_flask]

# 启动命令入口
command=/var/www/flask-point-system/venv/bin/uwsgi /var/www/flask-point-system/uwsgi-config.ini                                                                                                                                                                                
# 命令程序所在目录
directory=/var/www/flask-point-system/

#运行命令的用户名
user=root
autostart=true
autorestart=true

#日志地址
stdout_logfile=/var/www/flask-point-system/uwsgi_supervisor.log
```
配置完成后，我们可以执行以下命令启动服务和终止服务。
```
sudo service supervisor start
sudo service supervisor stop
```
我们执行 `sudo service supervisor start` 命令来启动服务。

#### 安装 Nginx 依赖库
```
# PCRE 库支持正则表达式。如果我们在配置文件 nginx.conf 中使用了正则表达式，那么在编译 Nginx 时就必须把 PCRE 库编译进 Nginx，因为 Nginx 的 HTTP 模块需要靠它来解析正则表达式。另外，pcre-devel 是使用 PCRE 做二次开发时所需要的开发库，包括头文件等，这也是编译 Nginx 所必须使用的。
sudo apt install libpcre3 libpcre3-dev
# zlib 库用于对 HTTP 包的内容做 gzip 格式的压缩，如果我们在 nginx.conf 中配置了 gzip on，并指定对于某些类型（content-type）的 HTTP 响应使用 gzip 来进行压缩以减少网络传输量，则在编译时就必须把 zlib 编译进 Nginx。zlib-devel 是二次开发所需要的库。
sudo apt install zlib1g-dev
# 如果服务器不只是要支持 HTTP，还需要在更安全的 SSL 协议上传输 HTTP，那么需要拥有 OpenSSL。另外，如果我们想使用 MD5、SHA1 等散列函数，那么也需要安装它。
sudo apt install openssl libssl-dev
```

#### 安装 Nginx
```
# 切换目录
cd /usr/local/src

# 下载源码
wget http://nginx.org/download/nginx-1.12.2.tar.gz

# 解压
tar -zxvf nginx-1.12.2.tar.gz

# 添加用户
useradd nginx

# 切换目录
cd nginx-1.12.2/

# 配置
./configure --prefix=/usr/local/nginx --user=nginx --group=nginx --with-http_ssl_module

# 编译安装
make && make install

# 创建软链接
ln -s /usr/local/nginx/sbin/nginx /usr/sbin

# 启动
nginx

# 查看 nginx 是否启动成功
netstat -anptu

# 停止 nginx
pkill -9 nginx
```

#### 配置 Nginx
关于 Nginx 的配置，推荐一篇博文[Nginx 配置简述](https://www.barretlee.com/blog/2016/11/19/nginx-configuration-start/)，这里给出了最简配置，
```
events {

}

http {
    server {
        listen 8888;  # nginx 监听的端口
        server_name XXX.XXX.XXX.XXX;  # 公网 ip
        location / {
            include  uwsgi_params;
            uwsgi_pass 127.0.0.1:8001;  # 指向 uwsgi 所应用的内部地址,所有请求将转发给 uwsgi 处理
            uwsgi_param UWSGI_PYHOME /var/www/flask-point-system/venv/;
            uwsgi_param UWSGI_CHDIR  /var/www/flask-point-system/;
            uwsgi_param UWSGI_SCRIPT manage:app;
        }
    }
}
```
配置完成后，重新启动下 nginx，在浏览器输入**公网ip:8888**就能看到项目主页了。

#### 数据库初始化
打开数据库客户端，执行以下命令，初始化数据库，用户测试、学习。
```
source init.sql
```

#### 生成 requirements.txt
开发完成要生成自己的 requirements.txt 文件，有以下两种方式。
```
# 方式一
pip install pipreqs
pipreqs ./

# 方式二
pip freeze > ./requirements.txt
```

#### 项目中用到的正则规则
1. 初始化分数（额度）可以为 0分 或者非 0 开头的 1~9 位数
2. 每次修改分数（额度）可以为非 0 开头的 1~4 位数，不能为 0 分
3. 账号只包含字母和数字，长度在 3-20 之间
4. 密码只包含字母和数字，长度在 6-20 之间
5. 姓名只能包含汉字，长度在 2-4 之间
6. 手机号码长度为 11 位，第一位必须为 1，第二位可为 3、4、5、7、8 

#### 该项目待完善部分
- 密码密文处理
- 服务器端合法性验证
- 404 错误页

#### 参考
1. [jQuery](https://www.jquery123.com/)
2. [Bootstrap](https://v2.bootcss.com/index.html)
3. [Flask](http://docs.jinkan.org/docs/flask/)
4. [菜鸟教程](http://www.runoob.com/)
5. [python 操作 MySQL](http://www.runoob.com/python/python-mysql.html)
6. [最全正则表达式总结：验证QQ号、手机号、Email、中文、邮编、身份证、IP地址等](http://www.lovebxm.com/2017/05/31/RegExp/)

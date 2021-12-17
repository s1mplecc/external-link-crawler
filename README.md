## 项目介绍

网站外链爬虫，使用轻量级 Web 应用框架 Flask，以 Restful 接口提供服务，支持容器化部署。

前提条件：需要 Python 版本 3.x。

对于传入的网站 URL，获取其 HTML 网页，提取外部链接的域名。包含如下几类外链：

- 超链接，标签 `a` 下的 `href` 属性；
- 图片，标签 `img` 下的 `src` 属性；
- 外部样式文件，标签 `link` 下  `href` 属性；
- 外部 JavaScript 脚本文件，标签 `script` 下  `src` 属性。

## 本地运行

Step 1：克隆项目。

```shell
$ git clone https://github.com/s1mplecc/external-link-crawer.git
```

Step 2：安装依赖，包括 Flask 和 BeautifulSoup4。建议使用 Virtualenv 局部安装依赖。

```shell
$ pip3 install -r requirements.txt 
```

Step 3：在 IDE 中运行或通过 Flask 命令行工具启动应用，端口号默认为 5000。生产环境可使用 Gunicorn 部署。

```shell
$ export FLASK_ENV="development"
$ flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## 容器化部署

除本地运行之外，也支持在生产环境中使用容器化方式部署，镜像入口脚本如下：

```shell
#!/bin/sh
gunicorn --worker-class=gevent --worker-connections=1000 -w 4 -b 0.0.0.0:8000 app:app
```

使用 Gunicorn 启动 Flask 应用。由于爬虫运行效率主要受网络延迟影响，因此为提高并发吞吐量，使用多进程 + 协程方式部署。协程由 Gevent 库支持。参数 `-w` 指定进程数，每个进程默认最大并发连接数
1000。Gunicorn 应用端口号默认为 8000。

Step 1：拉取镜像。镜像已提交至 Docker Hub 仓库。

```shell
$ docker pull s1mplecc/external-link-crawer
```

也可以手动构建镜像。克隆下项目后，在 Dockerfile 所在目录执行：

```shell
$ docker build -t s1mplecc/external-link-crawer .
```

Step 2：启动容器，映射端口。

```shell
$ docker run -d -p 5000:8000 --name external-link-crawer s1mplecc/external-link-crawer
```

## 请求格式

- 请求类型 GET；

- 请求前缀 `/external-link-domains` ；

- 参数 `url`，需传入合法 URL，否则返回参数异常状态码。

```shell
$ curl -XGET "http://127.0.0.1:5000/external-link-domains?url=https://www.zhihu.com/"
```

## 响应格式

响应体为 JSON 格式，包含如下字段：

- `data` 字段，数据本体；
- `code` 字段，状态码。成功 - 200，参数异常 - 400，服务器内部错误 - 500；
- `messages` 字段，附加消息。出错时提示异常信息。

响应样例如下：

```json
{
    "code": 200,
    "data": {
        "css_scripts_domains": [
            "hm.baidu.com",
            "static.zhihu.com"
        ],
        "css_scripts_domains_size": 2,
        "href_domains": [
            "app.mokahr.com",
            "beian.miit.gov.cn",
            "tsm.miit.gov.cn",
            "www.12377.cn",
            "www.beian.gov.cn",
            "www.zhihu.com",
            "zhstatic.zhihu.com",
            "zhuanlan.zhihu.com"
        ],
        "href_domains_size": 8,
        "img_domains": [
            "pic2.zhimg.com",
            "pic3.zhimg.com"
        ],
        "img_domains_size": 2
    },
    "messages": "[SUCCESS] ok"
}
```

参数异常响应样例如下：

```json
{
    "code": 400,
    "data": null,
    "messages": "[BAD_REQUEST] invalid param url value: xyz"
}
```

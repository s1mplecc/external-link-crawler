## 前言

网站外链爬虫，使用轻量级 Web 应用框架 Flask，以 Restful 接口提供服务。

对于传入的网站 URL，获取其 HTML 网页，提取外部链接的域名。包含如下几类外链：

- 超链接，标签 `a` 下的 `href` 属性；
- 图片，标签 `img` 下的 `src` 属性；
- 外部样式文件，标签 `link` 下  `href` 属性；
- 外部 JavaScript 脚本文件，标签 `script` 下  `src` 属性。

## 运行

Step 1：克隆项目。

```shell
$ git clone https://github.com/s1mplecc/external-link-crawer.git
```

Step 2: 安装依赖，包括 Flask 和 beautifulsoup4。

```shell
$ pip3 install -r requirements.txt 
```

Step 3：启动 Flask 应用，生产环境可使用 Gunicorn 部署。需要 Python 版本 3.x。

```shell
$ flask run   
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## 请求格式

GET 请求，Flask 应用默认运行在 5000 端口。

- 请求前缀 `/external-link-domains` ；

- 参数 `url`，需传入合法 URL，否则返回参数异常状态码。

```shell
$ curl -XGET http://127.0.0.1:5000/external-link-domains\?url\=https://www.zhihu.com/
```

## 响应格式

响应体为 JSON 格式，包含如下字段：

- `data` 字段，数据本体；
- `status` 字段，状态码。成功 - 200，参数异常 - 400，服务器内部错误 - 500；
- `msg` 字段，附加消息。出错时提示异常信息。

响应样例如下：

```json
{
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
  "msg": "[SUCCESS] ok",
  "status": 200
}
```

参数异常响应样例如下：

```json
{
  "data": null,
  "msg": "[BAD_REQUEST] invalid param url value: xyz",
  "status": 400
}
```


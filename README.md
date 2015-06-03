# zhihu-py3 : 知乎解析器 with Python3

## 介绍

前几天最近想写个小东西跟踪一下知乎上答案的点赞数增加曲线，可惜知乎没有API，搜索后发现 [zhihu-python][zhihu-python-url] 这个项目，奈何我一直用的Python3，于是乎重新造了个轮子。

功能和 [zhihu-python][zhihu-python-url] 类似，可以获取知乎上的信息和批量导出答案。

目前提供导出答案的 html 和 markdown 功能。

嘛，刚刚去增加了导出专栏文章的功能， markdown 格式。

因为写的急急忙忙可能会稍微有点小bug，如果有什么问题欢迎提 issue，当然 pull request 更好啦~

## 依赖

**依赖 [requests][req-url] 、[BeautifulSoup4][bs4-url]、[html2text][html2text-url] 使用前请先安装**

**PS： html2text 只在导出为 markdown 格式功能被使用时才会被 import，如果没有此模块其他功能也能正常完成。**

```bash
pip install requests
pip install beautifulsoup4
pip install html2text
```

在Ubuntu上,如果你同时安装了Pytho3和Pytho2,那么在impor zhihu的时候,会显示找不到bs4,之后还会有htm2tex的问题,这时候需要使用下面的命令安装:
```bash
sudo apt-get install python3-bs4
sudo apt-get install python3-html2text
```

**以下代码在 Windows 8.1 + Python3.4 + Beautifulsoup4 + requests + html2text环境下测试通过，其他环境未测试。**

2015.03.08 更新

**以下代码在 Kali Linux 1.1.0 (Debian 4.7.2-5) + Python 3.2.3 + Beautifulsoup4 + requests 环境下测试也通过了**

2015.06.03 更新  

**以下代码在 Ubuntu14.10 + Python3.4 + python3-bs4 + python3-html2text 测试通过

## 使用说明

### 准备工作

因为很重要所以说三遍

首次使用之前请先运行以下代码生成cookies文件：

首次使用之前请先运行以下代码生成cookies文件：

首次使用之前请先运行以下代码生成cookies文件：


```python
import zhihu

zhihu.create_cookies()
```

运行结果

```python
In [1]: import zhihu
no cookies file, this may make something wrong.
if you will run create_cookies or login next, please ignore me.

In [2]: zhihu.create_cookies()
email: <your-email-address>
password: <your-password>
please check code.gif
captcha: <captcha>
cookies file created!
```

运行成功后会在目录下生成cookies.json文件，请保持此文件和zhihu.py在同一目录下。

以下示例皆以正确生成了cookies文件为前提。

建议在正式使用之前运行zhihu-test.py测试一下。


### 快速备份

#### 备份某问题所有答案：

```python
import zhihu

question = zhihu.Question('http://www.zhihu.com/question/28092572')
for answer in question.answers:
    answer.save()
```

会在当前目录下新建以问题标题命名的文件夹，并将所有html文件保存到该文件夹。

save函数默认目录为当前目录下以问题标题命名的目录，默认文件名为问题标题加上答题者昵称，有相同昵称的情况下自动加上序号。

```python
answer.save(mode="md")
```
将会导出为markdown格式，下同。

#### 备份某用户所有答案：

```Python
import zhihu

author = zhihu.Author('http://www.zhihu.com/people/7sdream')
for answer in author.answers:
    # print(answer.question.title)
    answer.save(filepath=author.name)
```

会在当前目录下新建以作者昵称命名的文件夹，并将所有html文件保存到该文件夹。

#### 备份某收藏夹所有答案：

```Python
import zhihu

collection = zhihu.Collection('http://www.zhihu.com/collection/37770691')
for answer in collection.answers:
    # print(answer.question.title)
    answer.save(filepath=collection.name)
```

会在当前目录下新建以收藏夹名称命名的文件夹，并将所有html文件保存到该文件夹。

#### 备份某专栏所有文章：

```Python
import zhihu

book = zhihu.Book('http://zhuanlan.zhihu.com/xiepanda')

for article in book.posts:
    print(article.title)
    article.save(filepath=book.name)
```

会在当前目录下新建以专栏名命名的文件夹，并将所有md文件保存到该文件夹。

### 类简单用法说明

zhihu-py3 主要文件为 `zhihu.py`，配置文件为 `cookies.json` , 将这两个文件放到工作目录。

注：`cookies.json` 一般由 `create_cookies()` 函数创建，但也自己从浏览器中获取。

**嗯！类的用法请看 [zhihu-test.py][zhihu-test-py-url]，或者看[文档][doc-rtd-url]，就不在这里写啦**

### 其他常用方法

#### create_cookies

用于生成cookies，用法见前面的介绍

#### get_captcha_url

获取验证码url, 当用于其他项目时方便手动获取验证码图片进行处理

#### login

手动登陆方法，用于其他项目中方便手动无需cookies登陆，参数为：

 - email
 - password
 - captcha
 - savecookies 默认为 True

#### remove_invalid_char

删除字符串中不能出现在文件名中的字符，参数为要处理的字符串

可修改代码中的invalid_char_list来定义非法字符

## 文档

终于搞定了文档这个磨人的小妖精，可惜Sphinx还是不会用………… = = 先随意弄成这样吧：

Read The Docs： [点击这里查看文档][doc-rtd-url]

## TODO List

 - 写文档 T^T √
 - 增加导出为markdown功能 √
 - 增加获取答案点赞用户，用户关注者，用户追随者，收藏夹关注者，问题关注者等
 - 增加专栏类和文章类 √
 - 增加答案发布时间和更新时间的获取

## 更新日志

想了想还是加上这个吧，虽然经常一些小问题的修复也懒得写出来…………

2015.05.29：

修复了当问题关注人数为0时、问题答案数为0时的崩溃问题。（感谢：[段晓晨][thanks-zh-duan-xiao-chen-39]）

## 联系我

Github: [@7sDream][github-url]

知乎： [@7sDream][zhihu-url]

新浪微博：[@Dilover][weibo-url]

邮箱: [给我发邮件][mail-to-me]

[zhihu-python-url]: https://github.com/egrcc/zhihu-python
[req-url]: https://pypi.python.org/pypi/requests/2.5.1
[bs4-url]: http://www.crummy.com/software/BeautifulSoup
[html2text-url]: https://github.com/aaronsw/html2text
[doc-rtd-url]: http://zhihu-py3.readthedocs.org/zh_CN/latest/
[github-url]: https://github.com/7sDream
[weibo-url]: http://weibo.com/didilover
[zhihu-url]: http://www.zhihu.com/people/7sdream
[mail-to-me]: mailto:xixihaha.xiha@qq.com
[zhihu-test-py-url]: https://github.com/7sDream/zhihu-py3/blob/master/zhihu-test.py

[thanks-zh-duan-xiao-chen-39]: http://www.zhihu.com/people/duan-xiao-chen-39

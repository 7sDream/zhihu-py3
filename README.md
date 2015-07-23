# zhihu-py3 : 知乎解析器 with Python3

## DEV 分支更新


### 类名变更

专栏类从`Book`更名为`Cloumn`

文章类从`Article`更名为`Post`

以上两个更名同时影响了其他类的属性名，如`Author.books`变更为`Author.columns`，其他类同理。

### 接口名变更

1. 统一了一下复数的使用。比如`Author.answers_num`变为`Author.answer_num`, `Author.collections_num`变为`Author.collection_num`。也就是说某某数量的接口名为`Class.foo_num`，foo使用单数形式。

2. 知乎的赞同使用单词upvote，以前叫`agree`的地方现在都叫`upvote`。比如`Author.agree_num`变为`Author.upvote_num`, `Post.agree_num`变为`Post.upvote_num`

3. `Answer`类的`upvote`属性更名为`upvote_num`

### 提供`Topic`类

目前只有获取话题名的功能

### 提供`Author.activities` (测试特性)

属性获取用户动态，返回`Activity`类生成器。

`Activity`类提供`type`属性用于判断动态类型，`type`为`ActType`类定义的常量，根据`type`的不同提供不同的属性，如下表：

|类型|常量|提供的成员|
|:--:|:--:|---------:|
|关注了问题|FOLLOW_QUESTION|question|
|赞同了回答|UPVOTE_ANSWER|answer|
|关注了专栏|FOLLOW_COLUMN|book|
|回答了问题|ANSWER_QUESTION|answer|
|赞同了文章|UPVOTE_POST|article|
|关注了话题|FOLLOW_TOPIC|topic|
|提了一个问题|ASK_QUESTION|question|

示例代码见[zhihu-test.py][dev-zhihu-test-py-url]的`test_author`函数最后。

`activities`属性可以在未登录（未生成cookies）的情况下使用，但是根据知乎的隐私保护政策，开启了隐私保护的用户的回答和文章，此时作者信息会是匿名用户，所以还是建议登录后使用。

此功能还在测试期，欢迎各种test。

## 介绍

前几天最近想写个小东西跟踪一下知乎上答案的点赞数增加曲线，可惜知乎没有API，搜索后发现 [zhihu-python][zhihu-python-url] 这个项目，奈何我一直用的Python3，于是乎重新造了个轮子。

功能和 [zhihu-python][zhihu-python-url] 类似，可以获取知乎上的信息和批量导出答案。

目前提供导出答案的 html 和 markdown 功能。

嘛，刚刚去增加了导出专栏文章的功能， markdown 格式。

因为写的急急忙忙可能会稍微有点小 bug，如果有什么问题欢迎提 issue，当然 pull request 更好啦~

## 依赖

**依赖 [requests][req-url] 、[BeautifulSoup4][bs4-url]、[html2text][html2text-url] 使用前请先安装**

**html2text 只在导出为 markdown 格式功能被使用时才会被 import，如果没有此模块其他功能也能正常完成。**

```bash
pip install requests
pip install beautifulsoup4
pip install html2text
```

在 Ubuntu 上，如果你同时安装了 Python3 和 Python2，需要使用下面的命令安装：

```bash
sudo apt-get install python3-bs4
sudo apt-get install python3-html2text
```

或者使用

```bash
pip3 install requests
pip3 install beautifulsoup4
pip3 install html2text
```

## 使用说明

### 准备工作

因为很重要所以说三遍

首次使用之前请先运行以下代码生成 cookies 文件：

首次使用之前请先运行以下代码生成 cookies 文件：

首次使用之前请先运行以下代码生成 cookies 文件：


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

运行成功后会在目录下生成`cookies.json`文件，请保持此文件和`zhihu.py`在同一目录下。

以下示例皆以正确生成了 cookies 文件为前提。

建议在正式使用之前运行`zhihu-test.py`测试一下。


### 快速备份

#### 备份某问题所有答案：

```python
import zhihu

question = zhihu.Question('http://www.zhihu.com/question/28092572')
for answer in question.answers:
    answer.save()
```

会在当前目录下新建以问题标题命名的文件夹，并将所有html文件保存到该文件夹。

save 函数默认目录为当前目录下以问题标题命名的目录，默认文件名为问题标题加上答题者昵称，有相同昵称的情况下自动加上序号。

```python
answer.save(mode="md")
```
将会导出为 markdown 格式，下同。

#### 备份某用户所有答案：

```python
import zhihu

author = zhihu.Author('http://www.zhihu.com/people/7sdream')
for answer in author.answers:
    # print(answer.question.title)
    answer.save(filepath=author.name)
```

会在当前目录下新建以作者昵称命名的文件夹，并将所有 html 文件保存到该文件夹。

#### 备份某收藏夹所有答案：

```python
import zhihu

collection = zhihu.Collection('http://www.zhihu.com/collection/37770691')
for answer in collection.answers:
    # print(answer.question.title)
    answer.save(filepath=collection.name)
```

会在当前目录下新建以收藏夹名称命名的文件夹，并将所有 html 文件保存到该文件夹。

#### 备份某专栏所有文章：

```python
import zhihu

book = zhihu.Book('http://zhuanlan.zhihu.com/xiepanda')

for article in book.posts:
    print(article.title)
    article.save(filepath=book.name)
```

会在当前目录下新建以专栏名命名的文件夹，并将所有 md 文件保存到该文件夹。

### 类简单用法说明

zhihu-py3 主要文件为`zhihu.py`，配置文件为`cookies.json`, 将这两个文件放到工作目录。

注：`cookies.json`一般由`create_cookies()`函数创建，但也自己从浏览器中获取。

**嗯！类的用法请看 [zhihu-test.py][zhihu-test-py-url]，或者看[文档][doc-rtd-url]，就不在这里写啦**

### 其他常用方法

#### create_cookies

用于生成 cookies，用法见前面的介绍

#### get_captcha_url

获取验证码 url, 当用于其他项目时方便手动获取验证码图片进行处理

#### login

手动登陆方法，用于其他项目中方便手动无需 cookies 登陆，参数为：

 - email
 - password
 - captcha
 - savecookies 默认为 True

#### remove_invalid_char

删除字符串中不能出现在文件名中的字符，参数为要处理的字符串

可修改代码中的`invalid_char_list`来定义非法字符

## 文档

终于搞定了文档这个磨人的小妖精，可惜 Sphinx 还是不会用 T^T 先随意弄成这样吧：

Read The Docs： [点击这里查看文档][doc-rtd-url]

## TODO List

 - 写文档 T^T √
 - 增加导出为 markdown 功能 √
 - 增加专栏类和文章类 √
 - 增加获取用户最新动态功能 √
 - 增加获取答案点赞用户，用户关注者，用户追随者，收藏夹关注者，问题关注者等
 - 增加答案发布时间和更新时间的获取（这三个TODO准备暑假写掉，欢迎大家一起来 耶）

## 更新日志

想了想还是加上这个吧，虽然经常一些小问题的修复也懒得写出来…………

2015.07.23

1. 更改了一堆类名，接口名

2. 增加了Topic类，表示话题，功能只有获取话题名

3. 增加了Activity类，ActType常量类，用于处理用户动态

更新详情见文章开头。

2015.07.22

尝试修复了最新版bs4导致的问题，虽然我没明白问题在哪QuQ，求测试。

 - Windows 已测试 ([@7sDream][my-github-url])
 - Linux
    - Ubuntu 已测试([@7sDream][my-github-url])
 - Mac 已测试 ([@SimplyY][SimplyY-github-url])

2015.07.16

重构 Answer 和 Article 的 url 属性为 public.

2015.07.11:

Hotfix， 知乎更换了登录网址，做了简单的跟进，过了Test，等待Bug汇报中。

2015.06.04：

由[Gracker][gracker-github-url]补充了在 Ubuntu 14.04 下的测试结果，并添加了补充说明。

2015.05.29：

修复了当问题关注人数为0时、问题答案数为0时的崩溃问题。（感谢：[段晓晨][duan-xiao-chen-zhihu-url]）

## 联系我

Github: [@7sDream][my-github-url]

知乎： [@7sDream][my-zhihu-url]

新浪微博：[@Dilover][my-weibo-url]

邮箱: [给我发邮件][mail-to-me]

[zhihu-python-url]: https://github.com/egrcc/zhihu-python
[req-url]: https://pypi.python.org/pypi/requests/2.5.1
[bs4-url]: http://www.crummy.com/software/BeautifulSoup
[html2text-url]: https://github.com/aaronsw/html2text
[doc-rtd-url]: http://zhihu-py3.readthedocs.org/zh_CN/latest/
[zhihu-test-py-url]: https://github.com/7sDream/zhihu-py3/blob/master/zhihu-test.py
[dev-zhihu-test-py-url]: https://github.com/7sDream/zhihu-py3/blob/dev/zhihu-test.py

[my-github-url]: https://github.com/7sDream
[my-weibo-url]: http://weibo.com/didilover
[my-zhihu-url]: http://www.zhihu.com/people/7sdream
[mail-to-me]: mailto:xixihaha.xiha@qq.com
[duan-xiao-chen-zhihu-url]: http://www.zhihu.com/people/loveQt
[gracker-github-url]: https://github.com/Gracker
[SimplyY-github-url]: https://github.com/SimplyY

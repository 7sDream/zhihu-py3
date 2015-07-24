# zhihu-py3 : 知乎解析器 with Python3

[![Documentation Status][dev-doc-badge-img]][dev-doc-badge-url]

**说明：2015.07.24 对代码进行了比较大的重构，更新前请务必查看[ChangeLog][dev-changelog-url]**

## 功能

由于知乎没有公开API，加上受到[zhihu-python][zhihu-python-url]项目的启发，在Python3下重新写了一个知乎的数据解析模块。

提供的功能一句话概括为，用户提供知乎的网址构用于建对应类的对象，可以获取到某些需要的数据。

简单例子：

```python
url = 'http://www.zhihu.com/question/24825703'
question = zhihu.Question(url)

print(question.title)
print(question.answer_num)
print(question.follower_num)
print(question.topics)

for answer in question.answers:
    print(answer.author.name, answer.upvote_num)
```

这段代码的输出为：
```
关系亲密的人之间要说「谢谢」吗？
630
4316
['心理学', '恋爱', '社会', '礼仪', '亲密关系']
小不点儿 197
龙晓航 49
芝士就是力量 89
欧阳忆希 424
甜阁下 1155
```

另外还有`Author`、`Answer`、`Collection`、`Column`、`Post`、`Topic`等类可以使用，`Answer`,`Post`类提供了`save`方法能将答案或文章保存为HTML或Markdown格式，具体请看文档，或者`zhihu-test.py`

## 依赖

**本项目依赖于 [requests][req-url] 、[BeautifulSoup4][bs4-url]、[html2text][html2text-url] 使用前请先安装**

**html2text 只在导出为 markdown 格式功能被使用时才会被 import，如果没有此模块其他功能也能正常完成。**

```bash
pip install requests
pip install beautifulsoup4
pip install html2text
```

Linux下同时安装了Python2和3的用户请使用`pip3 install xxx`代替（应该不用我说……）

## 准备工作

首次使用之前请先运行以下代码生成 cookies 文件：

```python
import zhihu

zhihu.create_cookies()
```

运行结果

```ipython
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

## 用法实例

### 备份某问题所有答案：

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

### 备份某用户所有答案：

```python
import zhihu

author = zhihu.Author('http://www.zhihu.com/people/7sdream')
for answer in author.answers:
    # print(answer.question.title)
    answer.save(filepath=author.name)
```

备份某收藏夹所有答案，备份专栏文章同理，不再举例。

### 获取点赞的动态

```python
import zhihu

author = zhihu.Author('http://www.zhihu.com/people/rainy-vczh')
for act in author.activities:
    if act.type == zhihu.ActType.UPVOTE_ANSWER:
        print('%s 在 %s 赞同了问题 %s 中 %s(motto: %s) 的回答, '
              '此回答赞同数 %d' %
              (author.name, act.time, act.answer.question.title,
               act.answer.author.name, act.answer.author.motto,
               act.answer.upvote_num))
```

结果

```
vczh 在 2015-07-24 08:35:06 赞同了问题 女生夏天穿超短裙是一种什么样的体验？ 中 Light(motto: 我城故事多。) 的回答, 此回答赞同数 43
vczh 在 2015-07-24 08:34:30 赞同了问题 女生夏天穿超短裙是一种什么样的体验？ 中 Ms狐狸(motto: 随便写来玩玩) 的回答, 此回答赞同数 57
vczh 在 2015-07-24 06:43:49 赞同了问题 为什么好多中学生浑浑噩噩还不知悔改？ 中 胖子邓(motto: living, writing, loving.) 的回答, 此回答赞同数 1162
vczh 在 2015-07-24 06:33:42 赞同了问题 真皮座椅的汽车到底应不应该放座套？ 中 赵奕寒(motto: Safe Choix项目发起人) 的回答, 此回答赞同数 44
……
```

用户activities属性的完整用法课查看`zhihu-test.py`中`test_author`函数

## 其他常用方法

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

Read The Docs： [点击这里查看文档][dev-doc-rtd-url]

## TODO List

 - 增加获取答案点赞用户功能
 - 增加获取用户关注者，用户追随者，收藏夹关注者，问题关注者等等

## 联系我

Github：[@7sDream][my-github-url]

知乎：[@7sDream][my-zhihu-url]

新浪微博：[@Dilover][my-weibo-url]

邮箱：[给我发邮件][mail-to-me]

编程交流群：478786205

[zhihu-python-url]: https://github.com/egrcc/zhihu-python
[req-url]: https://pypi.python.org/pypi/requests/2.7.0
[bs4-url]: http://www.crummy.com/software/BeautifulSoup
[html2text-url]: https://github.com/aaronsw/html2text
[doc-rtd-url]: http://zhihu-py3.readthedocs.org/zh_CN/latest
[zhihu-test-py-url]: https://github.com/7sDream/zhihu-py3/blob/master/zhihu-test.py
[doc-badge-img]: https://readthedocs.org/projects/zhihu-py3/badge/?version=latest
[doc-badge-url]: https://readthedocs.org/projects/zhihu-py3/?badge=latest
[changelog-url]: https://github.com/7sDream/zhihu-py3/blob/master/ChangeLog.md

[my-github-url]: https://github.com/7sDream
[my-weibo-url]: http://weibo.com/didilover
[my-zhihu-url]: http://www.zhihu.com/people/7sdream
[mail-to-me]: mailto:xixihaha.xiha@qq.com

[dev-doc-rtd-url]: http://zhihu-py3.readthedocs.org/zh_CN/dev
[dev-zhihu-test-py-url]: https://github.com/7sDream/zhihu-py3/blob/dev/zhihu-test.py
[dev-doc-badge-img]: https://readthedocs.org/projects/zhihu-py3/badge/?version=dev
[dev-doc-badge-url]: https://readthedocs.org/projects/zhihu-py3/?badge=dev
[dev-changelog-url]: https://github.com/7sDream/zhihu-py3/blob/dev/ChangeLog.md

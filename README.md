# zhihu-py3 : 知乎解析器 with Python3

## 介绍

前几天最近想写个小东西跟踪一下知乎上答案的点赞数增加曲线，可惜知乎没有API，搜索后发现 [zhihu-python][zhihu-python-url] 这个项目，奈何我一直用的Python3，于是乎重新造了个轮子。

功能和 [zhihu-python][zhihu-python-url] 类似，可以获取知乎上的信息和批量导出答案。

目前只提供导出html，导出为markdown功能正在施工中。

## 依赖

**依赖 [requests][req-url] 、[BeautifulSoup4][bs4-url] 使用前请先安装**

```bash
pip install requests
pip install beautifulsoup4
```

**以下代码在 Windows 8.1 + Python3.4 + Beautifulsoup4 + requests 环境下测试通过，其他环境未测试。**

## 使用说明

### 准备工作


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


### 快速备份

#### 备份某问题所有答案：

```python
import zhihu

question = zhihu.Question('http://www.zhihu.com/question/28092572')
for answer in question.answers:
    answer.save()
```

会在当前目录下新建以问题标题命名的文件夹，并将所有html文件保存到该文件夹。

save函数默认目录为当前目录下以问题标题开头的目录，默认文件名为问题标题加上答题者昵称，有相同昵称的情况下自动加上序号。

#### 备份某用户所有答案：

```Python
import zhihu

author = zhihu.Author('http://www.zhihu.com/people/7sdream')
for answer in author.answers:
    # print(answer.question.title)
    answer.save(path=author.name)
```

会在当前目录下新建以作者昵称命名的文件夹，并将所有html文件保存到该文件夹。

#### 备份某收藏夹所有答案：

```Python
import zhihu

collection = zhihu.Collection('http://www.zhihu.com/collection/37770691')
for answer in collection.answers:
    # print(answer.question.title)
    answer.save(path=collection.name)
```

会在当前目录下新建以收藏夹名称命名的文件夹，并将所有html文件保存到该文件夹。

### 类简单用法说明

zhihu-python 主要文件为 `zhihu.py`，配置文件为 `cookies.json` , 将这两个文件放到工作目录。

注：`cookies.json` 一般由 `create_cookies()` 函数创建，但也自己从浏览器中获取。

#### Question 问题类

Question 代表一个问题，处理知乎问题相关操作。创建一个 Question 对象需传入该问题的 url ，如：

```python
from zhihu import Question

url = 'http://www.zhihu.com/question/24825703'
question = Question(url)
```

取得问题对象后可以获取一些信息

```python
# 获取该问题的详细描述
print(question.title)
# 亲密关系之间要说「谢谢」吗？

# 获取该问题的详细描述
print(question.details)
# 从小父母和大家庭里，.......什么时候不该说"谢谢”？？

# 获取回答个数
print(question.answers_num)
# 174

# 获取关注该问题的人数
print(question.followers_num)
# 1419

# 获取该问题所属话题
print(question.topics)
# ['心理学', '恋爱', '社会', '礼仪', '亲密关系']

# 获取排名第一的回答
print(question.top_answer)
# <zhihu.Answer object at 0x03D28810>

# 获取排名前十的十个回答
print(question.top_i_answers(10))
# <generator object top_i_answers at 0x0391DDF0>

# 获取所有回答
print(question.answers)
# <generator object answers at 0x0391DDF0>

# generator 对象可迭代：
for answer in question.answers:
    # do something with answer
    # like print(answer.upvote)
    pass
```

#### Answer 答案类

Answer 代表一个问题，处理知乎答案相关操作。创建一个 Answer 对象需传入该答案的 url

url 形如：http://www.zhihu.com/question/24825703/answer/30975949

此链接可从答案最后【编辑于 xxxx-xx-xx】处，右键-复制链接获得。

```python
from zhihu import Answer

url = 'http://www.zhihu.com/question/24825703/answer/30975949'
answer = Answer(url)
```

取得答案对象后可以获取一些信息

```python
# 获取该答案所在问题
print(answer.question)
# <zhihu.Question object at 0x02E7E4F0>

# 获取该答案作者
print(answer.author)
# <zhihu.Author object at 0x02E7E110>

# 获取答案赞同数
print(answer.upvote)
# 107


# 获取答案内容的HTML
print(answer.content)
# <html>
# ....
# </html>

# 保存HTML
from os import getcwd
answer.save(getcwd())
# 当前目录下生成 "亲密关系之间要说「谢谢」吗？ - 甜阁下.html"

# Question 和 Author object 可执行相应操作，如：

print(answer.question.title)
# 亲密关系之间要说「谢谢」吗？

print(answer.author.name)
# 甜阁下
```

#### Author 用户类

Author 代表一个用户，处理用户相关操作。创建一个 Author 对象需传入该用户的 url ，如：

```python
from zhihu import Author

url = 'http://www.zhihu.com/people/7sdream'
author = Author(url)
```

得到 Author 对象后，可以获取该用户的一些信息：

```python
# 获取用户名称
print(author.name)
# 7sDream

# 获取用户介绍
print(author.motto)
# 二次元新居民/软件爱好者/零回答消灭者

# 获取用户关注人数
print(author.followees_num)
# 66

# 获取用户粉丝数
print(author.followers_num)
# 179

# 获取用户得到赞同数
print(author.agree_num)
# 1078

# 获取用户得到感谢数
print(author.thanks_num)
# 370

# 获取用户提问数
print(author.questions_num)
# 16

# 获取用户答题数
print(author.answers_num)
# 227

# 获取用户专栏文章数
print(author.post_num)
# 0

# 获取用户收藏夹数
print(author.collections_num)
# 5

# 获取用户所有提问
print(author.questions)
# <generator object questions at 0x0156BF30>

# 获取用户所有回答
print(author.answers)
# <generator object answers at 0x0156BF30>

# 获取用户所有收藏夹
print(author.collections)
# <generator object collections at 0x0156BF30>

# 对 generator 可执行迭代操作， 这里用Collection举例
for collection in author.collections:
    print(collection.name)
# 教学精品。
# 可以留着慢慢看～
# OwO
# 一句。
# Read it later
```

### Collection 收藏夹类

Collection 代表一个收藏夹，处理收藏夹相关操作。创建一个 Collection 对象需传入该收藏夹的 url ，如：

```python
from zhihu import Collection

url = 'http://www.zhihu.com/collection/37770691'
collection = Collection(url)
```

得到 Collection 对象后，可以获取该收藏夹的一些信息：

```python
# 获取收藏夹名字
print(collection.name)
# 教学精品。

# 获取收藏夹关注人数
print(collection.followers_num)
# 0

# 获取收藏夹创建者
print(collection.owner)
# <zhihu.Author object at 0x03EFDB70>

# 获取收藏夹内所有答案
print(collection.answers)
# <generator object answers at 0x03F00620>

# 获取收藏夹内所有问题
print(collection.questions)
# <generator object questions at 0x03F00620>

# Author 对象 和 questions generator 用法见前文
```

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

*详细文档正在编写中……*

终于搞定了，Sphinx还是不会用…………= = 先随意弄成这样吧：

Read The Docs： [点击这里查看文档][doc-rtd-url]

## TODO List

 - ~写文档 T^T~
 - 增加导出为markdown功能
 - 增加获取答案点赞用户，用户关注者，用户追随者，收藏夹关注者，问题关注者等
 - 增加用户最近X个答案，X个问题的获取函数
 - 增加专栏类和文章类
 - 增加答案发布时间和更新时间的获取

## 联系我

Github: [@7sDream][github-url]

知乎： [@7sDream][zhihu-url]

新浪微博：[@Dilover][weibo-url]

邮箱: [给我发邮件][mail-to-me]

[zhihu-python-url]: https://github.com/egrcc/zhihu-python
[req-url]: https://pypi.python.org/pypi/requests/2.5.1
[bs4-url]: http://www.crummy.com/software/BeautifulSoup
[pillow-url]: https://pypi.python.org/pypi/Pillow/2.7.0
[doc-rtd-url]: http://zhihu-py3.readthedocs.org/zh_CN/latest/zhihu.html#module-zhihu
[github-url]: https://github.com/7sDream
[weibo-url]: http://weibo.com/didilover
[zhihu-url]: http://www.zhihu.com/people/7sdream
[mail-to-me]: mailto:xixihaha.xiha@qq.com

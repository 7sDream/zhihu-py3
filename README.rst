zhihu-py3 : 知乎非官方API库 with Python3
========================================

|Author| |Build| |DocumentationStatus| |PypiVersion| |License| |PypiDownloadStatus|

**紧急：知乎改用 https 了，遇到 invalid url 的朋友们请尽快 pypi 更新到 0.3.3 以上版本！**

Dev 分支coding内容：

 - unittest
 - 忙着跟上知乎的节奏（dog fuck's zhihu）


具体请看\ `ChangeLog <https://github.com/7sDream/zhihu-py3/blob/master/ChangeLog.rst>`__\ 。

**有问题请开Issue，几个小时后无回应可加最后面的QQ群询问。**

友链：

-  \ `zhihurss <https://github.com/SimplyY/zhihu-rss>`__\ ：一个基于 zhihu-py3 做的跨平台知乎 rss(any user) 的客户端。

功能
----

由于知乎没有公开API，加上受到\ `zhihu-python <https://github.com/egrcc/zhihu-python>`__\ 项目的启发，在Python3下重新写了一个知乎的数据解析模块。

提供的功能一句话概括为，用户提供知乎的网址构用于建对应类的对象，可以获取到某些需要的数据。

简单例子：

..  code:: python

    from zhihu import ZhihuClient

    Cookies_File = 'cookies.json'

    client = ZhihuClient(Cookies_File)

    url = 'http://www.zhihu.com/question/24825703'
    question = client.question(url)

    print(question.title)
    print(question.answer_num)
    print(question.follower_num)
    print(question.topics)

    for answer in question.answers:
        print(answer.author.name, answer.upvote_num)

这段代码的输出为：

::

    关系亲密的人之间要说「谢谢」吗？
    627
    4322
    ['心理学', '恋爱', '社会', '礼仪', '亲密关系']
    龙晓航 50
    小不点儿 198
    芝士就是力量 89
    欧阳忆希 425
    ...

另外还有\ ``Author（用户）``\ 、\ ``Answer（答案）``\ 、\ ``Collection（收藏夹）``\ 、\ ``Column（专栏）``\ 、\ ``Post（文章）``\ 、\ ``Topic（话题）``\ 等类可以使用，\ ``Answer``,\ ``Post``\ 类提供了\ ``save``\ 方法能将答案或文章保存为HTML或Markdown格式，具体请看文档，或者\ ``zhihu-test.py``\ 。

安装
----

..  class:: bold

   本项目依赖于\ `requests <https://pypi.python.org/pypi/requests/2.7.0>`__\ 、\ `BeautifulSoup4 <http://www.crummy.com/software/BeautifulSoup>`__\ 、\ `html2text <https://github.com/aaronsw/html2text>`__

已将项目发布到pypi，请使用下列命令安装

..  code:: bash

    (sudo) pip(3) install (--upgrade) zhihu-py3

希望开启lxml的话请使用：

..  code:: bash

    (sudo) pip(3) install (--upgrade) zhihu-py3[lxml]


因为lxml解析html效率高而且容错率强，在知乎使用\ ``<br>``\ 时，自带的html.parser会将其转换成\ ``<br>...</br>``\ ，而lxml则转换为\ ``<br/>``\ ，更为标准且美观，所以推荐使用第二个命令。

不安装lxml也能使用本模块，此时会自动使用html.parser作为解析器。

PS 若在安装lxml时出错，请安装libxml和libxslt后重试：

..  code:: bash

    sudo apt-get install libxml2 libxml2-dev libxslt1.1 libxslt1-dev

准备工作
--------

第一次使用推荐运行以下代码生成 cookies 文件：

..  code:: python

    from zhihu import ZhihuClient

    ZhihuClient().create_cookies('cookies.json')

运行结果

::

    ====== zhihu login =====
    email: <your-email>
    password: <your-password>
    please check captcha.gif for captcha
    captcha: <captcha-code>
    ====== logging.... =====
    login successfully
    cookies file created.

运行成功后会在目录下生成\ ``cookies.json``\ 文件。

以下示例皆以登录成功为前提。

建议在正式使用之前运行\ ``zhihu-test.py``\ 测试一下。

用法实例
--------

为了精简Readme，本部分移动至文档内。

请看文档的「用法示例」部分。

登录方法综述
---------------------------------------------

为了精简Readme，本部分移动至文档内。

请看文档的「登录方法综述」部分。

文档
----

终于搞定了文档这个磨人的小妖精，可惜 Sphinx 还是不会用 T^T
先随意弄成这样吧：

`Master版文档 <http://zhihu-py3.readthedocs.org/zh_CN/latest>`__

`Dev版文档 <http://zhihu-py3.readthedocs.org/zh_CN/dev>`__

TODO List
---------

- [x] 增加获取用户关注者，用户追随者
- [x] 增加获取答案点赞用户功能
- [x] 获取用户头像地址
- [x] 打包为标准Python模块
- [x] 重构代码，增加\ ``ZhihuClient``\ 类，使类可以自定义cookies文件
- [x] 收藏夹关注者，问题关注者等等
- [x] ``ZhihuClient``\ 增加各种用户操作（比如给某答案点赞）
- [ ] Unittest （因为知乎可能会变，所以这个有点难
- [x] 增加获取用户关注专栏数和关注专栏的功能
- [x] 增加获取用户关注话题数和关注话题的功能
- [x] 评论类也要慢慢提上议程了吧

联系我
------

Github：\ `@7sDream <https://github.com/7sDream>`__

知乎：\ `@7sDream <http://www.zhihu.com/people/7sdream>`__

新浪微博：\ `@Dilover <http://weibo.com/didilover>`__

邮箱：\ `给我发邮件 <mailto:xixihaha.xiha@qq.com>`__

编程交流群：478786205

.. |Author| image:: https://img.shields.io/badge/Author-7sDream-blue.svg
   :target: https://github.com/7sDream
.. |DocumentationStatus| image:: https://readthedocs.org/projects/zhihu-py3/badge/?version=latest
   :target: https://readthedocs.org/projects/zhihu-py3/?badge=latest
.. |PypiVersion| image:: https://img.shields.io/pypi/v/zhihu-py3.svg
   :target: https://pypi.python.org/pypi/zhihu-py3
.. |PypiDownloadStatus| image:: https://img.shields.io/pypi/dd/zhihu-py3.svg
   :target: https://pypi.python.org/pypi/zhihu-py3
.. |License| image:: https://img.shields.io/pypi/l/zhihu-py3.svg
   :target: https://github.com/7sDream/zhihu-py3/blob/master/LICENSE
.. |Build| image:: https://travis-ci.org/7sDream/zhihu-py3.svg?branch=dev
   :target: http://www.zhihu.com/people/7sdream

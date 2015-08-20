zhihu-py3 : 知乎非官方API库 with Python3
========================================

|Documentation Status|

最近一次更新内容：增加了Me类及其操作，增加了Topic类的功能。

具体请看\ `ChangeLog <https://github.com/7sDream/zhihu-py3/blob/master/ChangeLog.rst>`__\ 。

**有问题请开Issue，几个小时后无回应可加最后面的QQ群询问。**

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

以下示例均显示了使用cookies文件（上文生成）的登录方式，其他登录方式见后。

获取某用户的基本信息
~~~~~~~~~~~~~~~~~~~~

..  code:: python

    from zhihu import ZhihuClient

    Cookies_File = 'cookies.json'

    client = ZhihuClient(Cookies_File)

    url = 'http://www.zhihu.com/people/zord-vczh'
    author = client.author(url)

    print('用户名 %s' % author.name)
    print('用户简介 %s' % author.motto)
    print('用户关注人数 %d' % author.followee_num)
    print('取用户粉丝数 %d' % author.follower_num)
    print('用户得到赞同数 %d' % author.upvote_num)
    print('用户得到感谢数 %d' % author.thank_num)
    print('用户提问数 %d' % author.question_num)
    print('用户答题数 %d' % author.answer_num)

    print('用户专栏文章数 %d，名称分别为：' % author.post_num)
    for column in author.columns:
        print(column.name)
    print('用户收藏夹数 %d，名称分别为：' % author.collection_num)
    for collection in author.collections:
        print(collection.name)

结果：

::

    用户名 vczh
    用户简介 专业造轮子 https://github.com/vczh-libraries
    用户关注人数 1339
    取用户粉丝数 128100
    用户得到赞同数 320326
    用户得到感谢数 43045
    用户提问数 238
    用户答题数 8392
    用户专栏文章数 25，名称分别为：
    vczh的日常
    深井冰 IT 评论
    编程语言与高级语言虚拟机杂谈（仮）
    蓝色小药丸
    用户收藏夹数 1，名称分别为：
    李老师牛逼的答案

为节省篇幅，后文例子构建\ ``client``\ 的代码省略，因为都一样。

备份某问题所有答案
~~~~~~~~~~~~~~~~~~

..  code:: python

    question = client.question('http://www.zhihu.com/question/28092572')
    for answer in question.answers:
        answer.save()

会在当前目录下新建以问题标题命名的文件夹，并将所有html文件保存到该文件夹。

``save``\ 函数默认目录为当前目录下以问题标题命名的目录，默认文件名为问题标题加上答题者昵称，有相同昵称的情况下自动加上序号。

..  code:: python

    answer.save(mode="md")

将会导出为 markdown 格式，下同。

备份某用户所有答案
~~~~~~~~~~~~~~~~~~

..  code:: python

    author = client.author('http://www.zhihu.com/people/7sdream')
    for answer in author.answers:
        answer.save(filepath=author.name)

备份某收藏夹所有答案，备份专栏文章同理，不再举例。

获取某用户点赞的动态
~~~~~~~~~~~~~~~~~~~~

..  code:: python

    author = zhihu.author('http://www.zhihu.com/people/zord-vczh')
    for act in author.activities:
        if act.type == zhihu.ActType.UPVOTE_ANSWER:
            print('%s 在 %s 赞同了问题 %s 中 %s(motto: %s) 的回答, '
                  '此回答赞同数 %d' %
                  (author.name, act.time, act.answer.question.title,
                   act.answer.author.name, act.answer.author.motto,
                   act.answer.upvote_num))

结果

::

    vczh 在 2015-07-24 08:35:06 赞同了问题 女生夏天穿超短裙是一种什么样的体验？ 中 Light(motto: 我城故事多。) 的回答, 此回答赞同数 43
    vczh 在 2015-07-24 08:34:30 赞同了问题 女生夏天穿超短裙是一种什么样的体验？ 中 Ms狐狸(motto: 随便写来玩玩) 的回答, 此回答赞同数 57
    ……

用户activities属性的完整用法可查看\ ``zhihu-test.py``\ 中\ ``test_author``\ 函数

获取用户关注的人和关注此用户的人
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code:: python

    author = client.author('http://www.zhihu.com/people/7sdream')

    print('--- Followers ---')
    for follower in author.followers:
        print(follower.name)

    print('--- Followees ---')
    for followee in author.followees:
        print(followee.name)

结果：

::

    --- Followers ---
    yuwei
    falling
    周非
    ...
    --- Followees ---
    yuwei
    falling
    伍声
    ...

计算某答案点赞中三零用户比例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code:: python

    url = 'http://www.zhihu.com/question/30404450/answer/47939822'
    answer = client.answer(url)

    three_zero_user_num = 0

    for upvoter in answer.upvoters:
        print(upvoter.name, upvoter.upvote_num, upvoter.thank_num,
              upvoter.question_num, upvoter.answer_num)
        if upvoter.is_zero_user():
            three_zero_user_num += 1

    print('\n三零用户比例 %.3f%%' % (three_zero_user_num / answer.upvote_num * 100))

结果：

::

    ...
    宋飞 0 0 0 0
    唐吃藕 10 0 0 5

    三零用户比例 26.852%

爬取某用户关注的人的头像
~~~~~~~~~~~~~~~~~~~~~~~~

..  code:: python

    import requests
    import os
    import imghdr

    author = client.author('http://www.zhihu.com/people/zord-vczh')

    os.mkdir('vczh')
    for followee in author.followees:
        try:
            filename = followee.name + ' - ' + followee.id + '.jpeg'
            print(filename)
            with open('vczh/' + filename, 'wb') as f:
                f.write(requests.get(followee.photo_url).content)
        except KeyboardInterrupt:
            break

    for root, dirs, files in os.walk('vczh'):
        for filename in files:
            filename = os.path.join(root, filename)
            img_type = imghdr.what(filename)
            if img_type != 'jpeg' and img_type is not None:
                print(filename, '--->', img_type)
                os.rename(filename, filename[:-4] + img_type)

结果：

`点这里 <http://www.zhihu.com/question/28661987/answer/42591825>`__

登录相关方法（均为\ ``ZhihuClient``\ 的方法）
---------------------------------------------

create\_cookies
~~~~~~~~~~~~~~~

用于生成 cookies，用法见前面的介绍。

login\_with\_cookies
~~~~~~~~~~~~~~~~~~~~

用cookies字符串或文件名登录，\ ``ZhihuClient``\ 的构造函数就是使用这个方法。

get\_captcha
~~~~~~~~~~~~

获取验证码数据（bytes二进制数据），当用于其他项目时方便手动获取验证码图片数据进行处理，比如显示在控件内。

login
~~~~~

手动登陆方法，用于其他项目中方便手动无需 cookies 登陆，参数为：

-  email
-  password
-  captcha

返回值有三个

-  code：成功为0，失败为1
-  msg：错误消息，字符串格式，成功为空
-  cookies：cookies数据，字符串格式，失败为空

login\_in\_terminal
~~~~~~~~~~~~~~~~~~~

跟着提示在终端里登录知乎，返回cookies字符串，create\_cookies就是帮你做了将这个函数的返回值保存下来的工作而已。

综上
~~~~

如果你只是写个小脚本测试玩玩，可以使用：

..  code:: python

    from zhihu import ZhihuClient
    client = ZhiuhClien()
    client.login_in_terminal()

    # do thing you want with client

如果你的脚本不是大项目，又要多次运行，可以先按照上文方法create\_cookies，再使用：

..  code:: python

    from zhihu import ZhihuClient
    Cookies_File = 'cookies.json'
    client = ZhihuClient(Cookies_File)

如果项目比较大（以GUI项目为例），可以在判断出是首次使用（没有cookies文件）时，弹出登录对话框，使用get\_captcha获取验证码数据，再调用login函数手动登录并在登录成功后保存cookies文件：

..  code:: python

    import os
    from zhihu import ZhihuClient

    Cookies_File = 'config/cookies.json'

    client = ZhihuClient()

    def on_window_show()
        login_btn.disable()
        if os.path.isfile(Cookies_File) is False:
            captcha_imgbox.setData(client.get_capthca())
            login_btn.enable()
        else:
            with open(Cookies_File) as f
                client.login_with_cookies(f.read())
            # turn to main window

    def on_login_button_clicked():
        login_btn.disable()
        email = email_edit.get_text()
        password = password_edit.get_text()
        captcha = captcha_edit.get_text()
        code, msg, cookies = clien.login(email, password, captcha)
        if code == 0:
            with open(Cookies_File, 'w') as f
                f.write(cookies)
            # turn to main window
        else:
            msgbox(msg)
            login_btn.enable()

注：以上和GUI有关的代码皆为我乱想出来的，仅作示例之用。

文档
----

终于搞定了文档这个磨人的小妖精，可惜 Sphinx 还是不会用 T^T
先随意弄成这样吧：

Read The Docs：
`点击这里查看文档 <http://zhihu-py3.readthedocs.org/zh_CN/latest>`__

TODO List
---------

-  [x] 增加获取用户关注者，用户追随者
-  [x] 增加获取答案点赞用户功能
-  [x] 获取用户头像地址
-  [x] 打包为标准Python模块
-  [x] 重构代码，增加\ ``ZhihuClient``\ 类，使类可以自定义cookies文件
-  [x] 收藏夹关注者，问题关注者等等
-  [x] ``ZhihuClient``\ 增加各种用户操作（比如给某答案点赞）

联系我
------

Github：\ `@7sDream <https://github.com/7sDream>`__

知乎：\ `@7sDream <http://www.zhihu.com/people/7sdream>`__

新浪微博：\ `@Dilover <http://weibo.com/didilover>`__

邮箱：\ `给我发邮件 <mailto:xixihaha.xiha@qq.com>`__

编程交流群：478786205

.. |Documentation Status| image:: https://readthedocs.org/projects/zhihu-py3/badge/?version=latest
   :target: https://readthedocs.org/projects/zhihu-py3/?badge=latest

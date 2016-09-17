更新日志
========

0.3.23
------

- [Fix] 修复了由于知乎前端更改， `Activity` 类中获取 「提了一个问题」 类型的动态时会报错的 Bug。

0.3.22
------

- [Add] 增加了 `Author.followers_skip()` 和 `Author.followees.skip()` 函数，可以在获取用户关注者时跳过前 n 个用户。

0.3.21
------

- [Add] 增加了一个 `BanException` 异常，在尝试获取被反作弊系统限制的用户资料时将会引发此异常，需要用户自行处理。

0.3.20
------

- [fix] 修复获取用户粉丝时，因为新的徽章的加入造成的解析 Bug。

0.3.19
------

- [Fix] 现在允许通过 `https://www.zhihu.com/org/abcde` 这种 URL 获取机构号对象。
- [Add] `ZhihuClient.login_in_termianl` 和 `ZhihuClient.create_cookies` 增加了参数 `use_getpass` 来设置是否使用安全模式输入密码，以解决在某些 Windows 上的 IDE 中运行时无法输入密码的问题。。

0.3.18
------

- [fix] 修复了许多由知乎前端改变造成的小 bug，暂时又可用了。

0.3.17
------

- [fix] 修复答案翻页 pagesize 改变造成的无法获取所有答案的问题
- [fix] 修复了一大都因为前端 data-votecount 属性被删除造成的问题……
- [update] 改了一点测试代码……

0.3.16
------

- [fix] 修复因知乎登录又需要验证码且验证码逻辑小幅度修改造成的无法登录的问题

0.3.15
------

- [change] 现在 question.topics 返回 Topic 对象的迭代器，而不是话题名字的列表

0.3.14
------

- [fix] 修复 Author.columns 因为知乎专栏大幅度改版而无法获取到专栏的问题
- [fix] 修复 Post.column 因为知乎现在允许发布无专栏文章而出错的 bug，对于无专栏的 Post 现在 column 属性返回 None
- [fix] 修复 Post.slug 因为知乎文章网址变更而无法获取的问题
- [fix] 修复 Post.column_in_name 因为知乎现在允许发布无专栏文章而出错的 bug，对于无专栏的 Post 现在 column 属性返回 None
- [fix] 修复因为上述 Bugs 造成的 Author.activities 出错的问题
- [add] 现在 CollectActType 可以直接从模块顶级 import， 即 from zhihu import CollectActType
- [fix] 修复 Topic.follower.motto 获取不正确的问题

0.3.13
------

- [fix] 修复因知乎将每次点击问题页面「更多」按钮只加载 50 个回答改为 20 个造成的无法获取所有问题的 bug
- [fix] 修复获取 post 后，直接调用 post.save 会出错的 bug
- [change] 在终端登录时输入的密码改为不可见
- [change] 貌似知乎登录不怎么需要验证码了，现在作为一个可选项，login_in_terminal 和 create_cookies 默认均不要求验证码
- [fix] 修复因知乎专栏改版，API 地址变更 造成的 Post 类无法使用的问题
- [add] 增加 client.add_proxy_pool 方法设置代理池
- [add] 增加 client.remove_proxy_pool 方法移除代理池

0.3.12
------

- [rollback] 知乎又把所有问题的接口改回来了……妈的智障
- [add] 增加了获取话题下等待回答的问题的功能：Topic.unanswered_questions

0.3.11
------

- [add] Avoid redirection
- [fix] 知乎改了 Topic 的所有问题功能，变成等待回答的功能了

0.3.10-1
--------

- [fix] 我真是傻了，上传之前忘记删除debug语句了。。。

0.3.10
------
- [add] 添加 answer.latest_comments 属性
- [fix] 获取头像失败
- [add] zhihu.ANONYMOUS 表示匿名用户
- [fix] answer.deleted 属性错误
- [fix] 解决一些诡异的用户带来的问题
- [add] post 可保存为 html 格式
- [fix] 修复 Author 的 location education 等属性无法获取的 bug

0.3.9-1
-------

- [fix] 修复了由于 img 的 title 属性修改为 alt 属性造成的 Author.followed_topic 获取前几个话题出错的 bug

0.3.9
-----

- [add] Question 和 Answer 添加 deleted 属性
- [fix] 修复了问题没有回答时 Question.answers 出错的问题
- [fix] 修复了回答仅有一页时无法获取按时间排序的答案的问题
- [fix] 修复无法刷新 answer_num 的问题
- [fix] 修复收藏为0时获取收藏数出错的问题
- [fix] 知乎修改了评论的前端代码
- [change] Comment 类现在也提供 datetime.datetime 类型的 creation_time 属性, 去掉 time_string
- [fix] 修复了 topic.question 由于时间戳乘以了 1000 而造成的错误
- [fix] 修复了 topic.top_answer 无法获取到内容的 bug
- [fix] 修复了 topic.hot_answer 无法获取到内容的 bug

0.3.8
-----

- [add] Answer 和 Question 增加 refresh() 方法, 刷新问题答案 object 的属性
- [add] Question 初始化的 url 现在支持 ?sort=created
- [add] 使用带 ?sort=created 的 url 初始化问题时, question.answers 按照时间顺序返回答案
- [add] 添加了 Answer.comment_num 属性, 获取评论数量
- [add] 添加了 Collection.id 属性
- [fix] 现在 Activity.type 变成 read-only property 并加入文档了

全都 Thanks `@laike9m <https://github.com/laike9m>`__

0.3.7
-----

- [fix] 修复了用户动态中有关注圆桌行为时会崩溃的 Bug（目前暂时跳过这类动态）。
- [fix] 知乎删除了深网话题，正好Topic类是用的那个话题测试，我还以为代码bug了……现在改成测试「程序员」话题。
- [add] 曾加了获取专栏文章点赞者的功能。


0.3.6
-----

- [fix] 修试图获取登录用户自身 location, business 等属性但自己又未填写时出现的 bug
- [fix] 修复 topic.py 中混合使用 return sth 和 yield sth 导致的旧版本 python 报语法错误的问题
- [add/fix] ActType 中添加了关注收藏夹 (Thanks `@cssmlulu <https://github.com/cssmlulu>`__)
- [fix] 修复了 Author.activities 项 answer 的 author 属性不正确的 bug (Thanks `@cssmlulu <https://github.com/cssmlulu>`__)

0.3.5
-----

- [add] 添加 Answer.collect_num 属性, 获取答案的收藏数
- [add] 添加 Answer.collections 接口, 获取收藏了该答案的收藏夹
- [add] 添加 Collections.logs 接口, 获取收藏夹日志
- [add] 添加 Question.author 属性，获取提问者
- [fix] 修复文档代码的一些错误

前四个功能Thanks `@laike9m <https://github.com/laike9m>`__

0.3.4
-----

- [f**K] 随便在知乎上发了个小专栏……不小心就进撕逼大战了 QAQ 我好方～
- [add] 增加了 example 文件夹，里面放一些实例
- [add] Add answer creation_time attribute(Thanks @laike9m)
- [add] 添加 Question.creation_time 和 Question.last_edit_time 属性(Thanks @laike9m)
- [fix] 修复了 UPVOTE_ANSWER 型的 Activity 的 act.answer.author 全都是匿名用户的 bug（不知道是不是前端改了）

0.3.3
-----

- [fix] 紧急更新，知乎页面上的链接大多数都变成了 https, 暂时只简单的改了一点正则表达式已作为紧急应对，有 bug 请开 issue。

0.3.2
-----

- [change] 改变 Author 类获取 Activities 的机制，判断类型更准确(Thanks `@laike9m <https://github.com/laike9m>`__)。
- [change] 为方便以后写测试，类架构修改为均继承 BaseZhihu 类（Thanks `@littlezz <https://github.com/littlezz>`__)。

0.3.1
-----

- [fix] 修复因为知乎 Answer 的 css class 更改导致的 Answer 类 content 属性获取不正确的 bug
- [fix] 修复历史遗留代码造成使用 profile card 获取头像时，网址不正确的 bug（Thanks `@bdqy <https://github.com/bdqy>`__）
- [fix] 修复因答案被和谐造成的 bug（Thanks `@littlezz <https://github.com/littlezz>`__）
- [add] 获取用户的一些详细信息，包括微博，所在地，教育情况，所在行业等等(Thanks `@zeroxfio <https://github.com/zeroxfio>`__）
- [add] Answer 类增加了获取答案的评论的功能(Thanks `@zeroxfio <https://github.com/zeroxfio>`__）
- [add] Me 类增加了发送私信和评论的功能(Thanks `@zeroxfio <https://github.com/zeroxfio>`__）
- [add] Me 类增加了给答案点没有帮助的功能(Thanks `@lishubing <https://github.com/lishubing>`__)
- [add] Me 类增加了屏蔽用户，屏蔽话题的功能(Thanks `@lishubing <https://github.com/lishubing>`__)

0.3.0
-----

- [fix] 修复 Author 类的 get_followed_columns 接口获取到的 Column 对象调用 followed_num 函数可能获取不到正确数量的 bug
- [fix] 修复 Author 类的 get_followed_columns 接口获取到的 Column 对象处于未登录状态的 bug
- [add] Author 类增加获取用户关注的话题数的接口（followed_topic_num）
- [add] Author 类增加获取用户关注的话题的接口 （followed_topics）

0.2.9
-----

- [fix] 修复因问题描述和答案使用相同的 class 造成的答案内容与序号不同的 bug。
- [tucao] 一天修三四个bug好累……我估计得找时间抓一下知乎的移动端 API 了，前端天天变这谁受得了。

0.2.8
-----

- [fix] 上次的 bug 修复的不完全，匿名用户的情况没有考虑周全，紧急修复下……（可能还有地方没修复，请关注更新。

0.2.7
-----

- [fix] 修复由于把用户 tag 从 h3 改成了 div 造成的一系列 bug (Thanks `@lishubing <https://github.com/lishubing>`__)

0.2.6
-----

- [fix] 获取匿名用户的ID出错的问题，暂定为返回空字符串
- [add] 增加获取用户关注专栏数的功能 (Thanks `@cssmlulu <https://github.com/cssmlulu>`__)
- [add] 增加获取用户关注专栏的功能 (Thanks `@cssmlulu <https://github.com/cssmlulu>`__)

0.2.5
-----

- [fix] 修复了某些问题无法获取答案的bug
- [fix] 知乎又把头像链接改回去了。。。

0.2.4
-----

- [fix] 知乎修改了图片链接的格式，影响了答案图片，头像。

0.2.3
-----

- [fix] Topic.hot_question 的顺序 Bug
- [fix] 知乎登录逻辑修改（？）
- [add] Topic 所有答案接口
- [add] Topic 热门答案接口

0.2.2
-----

代码美化，尽量满足 PEP8.

0.2.1
-----

增加 Topic 类的最近动态（热门排序）
修复 Topic.children 的bug

0.2.0
-----

增加Me类及其相关操作

-  [x] 点赞，取消点赞，反对，取消反对某回答
-  [x] 点赞，取消点赞，反对，取消反对某文章
-  [x] 感谢，取消感谢某回答
-  [x] 关注，取消关注某用户
-  [x] 关注，取消关注某问题
-  [x] 关注，取消关注某话题
-  [x] 关注，取消关注收藏夹

增加Topic类相关操作：

-  [x] 获取话题名称
-  [x] 获取话题描述
-  [x] 获取话题图标
-  [x] 获取关注者数量
-  [x] 获取关注者
-  [x] 获取父话题
-  [x] 获取子话题
-  [x] 获取优秀答主
-  [ ] 获取最近动态（暂缓）
-  [x] 获取精华回答
-  [x] 获取所有问题

0.1.5
-----

- 增加了获取收藏夹关注者的功能
- 增加了获取问题关注者的功能
- Column的一个小Bug修复

0.1.4
-----

知乎登录参数变化，从rememberme变成了remember_me，做了跟进。

2015.07.30
----------

发布到Pypi.

2015.07.29
----------

-  重构项目结构
-  增加 zhihu.Client 类，改善原先模块需要使用当前目录下 cookies 的弊端，现在的使用方法请看 Readme 中的示例。
-  去掉了 _text2int 方法，因为发现知乎以K结尾的赞同数也有办法获取到准确点赞数。

2015.07.26
----------

重构项目结构，转变为标准 Python 模块结构。

2015.07.26
----------

添加 Author.photo_url 接口，用于获取用户头像。

本属性的实现较为分散，在不同的地方使用了不同的方法：

-  Author.follower(e)s, Answer.upvoters 等属性返回的 Author 自带 photo_url

-  用户自定义的 Author 在访问过主页的情况下通过解析主页得到

-  用户自定义的 Author 在未访问主页的情况下为了性能使用了知乎的 CardProfile
   API

因为实现混乱所以容易有Bug，欢迎反馈。

2015.07.25
----------

增加了获取用户关注者和粉丝的功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author.followers, Author.folowees 返回Author迭代器，自带url, name, motto, question\_num, answer\_num, upvote\_num, follower\_num属性。

html解析器优选
~~~~~~~~~~~~~~

在安装了 lxml 的情况下默认使用 lxml 作为解析器，否则使用 html.parser。

增加答案获取点赞用户功能
~~~~~~~~~~~~~~~~~~~~~~~~

Author.upvoters 返回 Author 迭代器，自带url, name, motto, question\_num, answer\_num, upvote\_num, thank\_num属性

增加简易判断是否为「三零用户」功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author.is_zero_user() ，判断标准为，赞同，感谢，提问数，回答数均为 0。

2015.07.23
----------

各个类url属性更改为公开
~~~~~~~~~~~~~~~~~~~~~~~

暂时这样吧，有点懒了，因为这样会让使用者有机会非法修改 url，可能导致 Bug，以后勤快的话会改成 read-only。

类名变更
~~~~~~~~

专栏类从 Book 更名为 Cloumn

文章类从 Article 更名为 Post

以上两个更名同时影响了其他类的属性名，如 Author.books 变更为 Author.columns，其他类同理。

接口名变更
~~~~~~~~~~

1. 统一了一下复数的使用。比如 Author.answers_num 变为 Author.answer_num, Author.collections\_num 变为 Author.collection\_num。
也就是说某某数量的接口名为 Class.foo_num，foo使用单数形式。

2. 知乎的赞同使用单词 upvote，以前叫 agree 的地方现在都叫 upvote。比如 Author.agree_num 变为 Author.upvote_num，Post.agree_num 变为 Post.upvote_num。

3. Answer 类的 upvote 属性更名为 upvote_num。

提供\ ``Topic``\ 类
~~~~~~~~~~~~~~~~~~~

目前只有获取话题名的功能。

提供\ ``Author.activities``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

属性获取用户动态，返回 Activity 类生成器。

Activity 类提供 type 属性用于判断动态类型，type 为 ActType 类定义的常量，根据 type 的不同提供不同的属性，如下表：

+----------------+--------------------+--------------+
| 类型           | 常量               | 提供的成员   |
+================+====================+==============+
| 关注了问题     | FOLLOW\_QUESTION   | question     |
+----------------+--------------------+--------------+
| 赞同了回答     | UPVOTE\_ANSWER     | answer       |
+----------------+--------------------+--------------+
| 关注了专栏     | FOLLOW\_COLUMN     | column       |
+----------------+--------------------+--------------+
| 回答了问题     | ANSWER\_QUESTION   | answer       |
+----------------+--------------------+--------------+
| 赞同了文章     | UPVOTE\_POST       | post         |
+----------------+--------------------+--------------+
| 发布了文章     | PUBLISH\_POST      | post         |
+----------------+--------------------+--------------+
| 关注了话题     | FOLLOW\_TOPIC      | topic        |
+----------------+--------------------+--------------+
| 提了一个问题   | ASK\_QUESTION      | question     |
+----------------+--------------------+--------------+

由于每种类型都只提供了一种属性，所以所有Activity对象都有 content 属性，用于直接获取唯一的属性。

示例代码见 zhihu-test.py 的 test_author 函数。

activities 属性可以在未登录（未生成cookies）的情况下使用，但是根据知乎的隐私保护政策，开启了隐私保护的用户的回答和文章，此时作者信息会是匿名用户，所以还是建议登录后使用。

2015.07.22
----------

尝试修复了最新版bs4导致的问题，虽然我没明白问题在哪QuQ，求测试。

-   Windows 已测试 (`@7sDream <https://github.com/7sDream>`__)
-   Linux

    -   Ubuntu 已测试(`@7sDream <https://github.com/7sDream>`__)

-   Mac 已测试(`@SimplyY <https://github.com/SimplyY>`__)

2015.07.16
----------

重构 Answer 和 Article 的 url 属性为 public.

2015.07.11:
-----------

Hotfix， 知乎更换了登录网址，做了简单的跟进，过了Test，等待Bug汇报中。

2015.06.04：
------------

由 `@Gracker <https://github.com/Gracker>`__ 补充了在 Ubuntu 14.04
下的测试结果，并添加了补充说明。

2015.05.29：
------------

修复了当问题关注人数为0时、问题答案数为0时的崩溃问题。（感谢：`@段晓晨 <http://www.zhihu.com/people/loveQt>`__）

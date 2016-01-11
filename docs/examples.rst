========
用法示例
========

..  contents:: 目录
    :local:


获取某用户的基本信息
====================

..  code-block:: python
    :linenos:
   
    from zhihu import ZhihuClient

    Cookies_File = 'cookies.json'

    client = ZhihuClient(Cookies_File)

    url = 'http://www.zhihu.com/people/excited-vczh'
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

..  code-block:: none
    :linenos:

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

备份某问题所有答案
==================
..  code-block:: python
    :linenos:
   
    question = client.question('http://www.zhihu.com/question/28092572')
    for answer in question.answers:
       answer.save()
       
会在当前目录下新建以问题标题命名的文件夹，并将所有html文件保存到该文件夹。

..  code-block:: python

    answer.save(mode="md")

会保存为markdown格式。

备份某用户所有答案
==================

..  code-block:: python
    :linenos:

    author = client.author('http://www.zhihu.com/people/7sdream')
    for answer in author.answers:
       answer.save(filepath=author.name)

备份某收藏夹所有答案，备份专栏文章同理，不再举例。

获取某用户点赞的动态
====================

..  code-block:: python
    :linenos:

    author = zhihu.author('http://www.zhihu.com/people/excited-vczh')
    for act in author.activities:
       if act.type == zhihu.ActType.UPVOTE_ANSWER:
           print('%s 在 %s 赞同了问题 %s 中 %s(motto: %s) 的回答, '
                 '此回答赞同数 %d' %
                 (author.name, act.time, act.answer.question.title,
                  act.answer.author.name, act.answer.author.motto,
                  act.answer.upvote_num))

..  code-block:: none

    vczh 在 2015-07-24 08:35:06 赞同了问题 女生夏天穿超短裙是一种什么样的体验？ 中 Light(motto: 我城故事多。) 的回答, 此回答赞同数 43
    vczh 在 2015-07-24 08:34:30 赞同了问题 女生夏天穿超短裙是一种什么样的体验？ 中 Ms狐狸(motto: 随便写来玩玩) 的回答, 此回答赞同数 57
    ……

获取用户关注的人和关注此用户的人
================================

..  code-block:: python
    :linenos:

    author = client.author('http://www.zhihu.com/people/7sdream')

    print('--- Followers ---')
    for follower in author.followers:
       print(follower.name)

    print('--- Followees ---')
    for followee in author.followees:
       print(followee.name)

..  code-block:: none

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
============================

..  code-block:: python
    :linenos:
   
    url = 'http://www.zhihu.com/question/30404450/answer/47939822'
    answer = client.answer(url)

    three_zero_user_num = 0

    for upvoter in answer.upvoters:
       print(upvoter.name, upvoter.upvote_num, upvoter.thank_num,
             upvoter.question_num, upvoter.answer_num)
       if upvoter.is_zero_user():
           three_zero_user_num += 1

    print('\n三零用户比例 %.3f%%' % (three_zero_user_num / answer.upvote_num * 100))
   
..  code-block:: none

    ...
    宋飞 0 0 0 0
    唐吃藕 10 0 0 5

    三零用户比例 26.852%

爬取某用户关注的人的头像
========================

..  code-block:: python

    import requests
    import os
    import imghdr

    author = client.author('http://www.zhihu.com/people/excited-vczh')

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

效果见 `这里
<http://pan.baidu.com/s/1i3nLgpB>`_。


使用非阻塞的网络请求
====================

内建的所有请求都是阻塞的, 如果你希望使用其他的网络请求方法, 你可以把请求到的数据传入相关类的 `from_html` 方法中.
`from_html` 方法用于接受数据, 返回相应的类的实例.

这里以使用 aiohttp 为例, 使用的是 python3.5 之后引入的语法. 无需置疑, 你要自己处理 session

比如要获取一个答案.

..  code-block:: python

    import aiohttp
    import asyncio
    import zhihu


    async def get_answer(url, cookies, headers):
        async with aiohttp.get(url, cookies=cookies, headers=headers) as r:
            data = await r.text()

        # from_html 是 classmethod
        answer = zhihu.Answer.from_html(data)

        print(answer.content)

    url = 'answer url'
    cookies = dict(client._session.cookies)
    headers = client._session.headers

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_answer(url, cookies, headers))



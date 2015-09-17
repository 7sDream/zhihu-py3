#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import os
import shutil
from zhihu import ZhihuClient, ActType


def test_question():
    url = 'http://www.zhihu.com/question/24825703'
    question = client.question(url)

    # 获取该问题的详细描述
    print(question.title)
    # 亲密关系之间要说「谢谢」吗？

    # 获取该问题的详细描述
    print(question.details)
    # 从小父母和大家庭里，.......什么时候不该说"谢谢”？？

    # 获取回答个数
    print(question.answer_num)
    # 630

    # 获取关注该问题的人数
    print(question.follower_num)
    # 4326

    # 获取关注问题的用户
    for _, follower in zip(range(0, 10), question.followers):
        print(follower.name)
    # J Drop
    # 熊猫
    # Steve He
    # ...

    # 获取该问题所属话题
    print(question.topics)
    # ['心理学', '恋爱', '社会', '礼仪', '亲密关系']

    # 获取排名第一的回答的点赞数
    print(question.top_answer.upvote_num)
    # 197

    # 获取排名前十的十个回答的点赞数
    for answer in question.top_i_answers(10):
        print(answer.author.name, answer.upvote_num)
    # 49
    # 89
    # 425
    # ...


def test_answer():
    url = 'http://www.zhihu.com/question/24825703/answer/30975949'
    answer = client.answer(url)

    # 获取答案url
    print(answer.url)

    # 获取该答案所在问题标题
    print(answer.question.title)
    # 关系亲密的人之间要说「谢谢」吗？

    # 获取该答案作者名
    print(answer.author.name)
    # 甜阁下

    # 获取答案赞同数
    print(answer.upvote_num)
    # 1155

    # 获取答案点赞人昵称和感谢赞同提问回答数
    for _, upvoter in zip(range(1, 10), answer.upvoters):
        print(upvoter.name, upvoter.upvote_num, upvoter.thank_num,
              upvoter.question_num, upvoter.answer_num, upvoter.is_zero_user())
    # ...
    # 五月 42 15 3 35
    # 陈半边 6311 1037 3 101
    # 刘柯 3107 969 273 36
    #
    # 三零用户比例 36.364%

    # 获取答案内容的HTML
    print(answer.content)
    # <html>
    # ...
    # </html>

    # 保存HTML
    answer.save(filepath='.')
    # 当前目录下生成 "亲密关系之间要说「谢谢」吗？ - 甜阁下.html"

    # 保存markdown
    answer.save(filepath='.', mode="md")
    # 当前目录下生成 "亲密关系之间要说「谢谢」吗？ - 甜阁下.md"


def test_author():
    url = 'http://www.zhihu.com/people/7sdream'
    author = client.author(url)

    # 获取用户名称
    print(author.name)
    # 7sDream

    # 获取用户介绍
    print(author.motto)
    # 二次元新居民/软件爱好者/零回答消灭者

    # 获取用户头像地址
    print(author.photo_url)
    # http://pic3.zhimg.com/893fd554c8aa57196d5ab98530ef479a_r.jpg

    # 获取用户得到赞同数
    print(author.upvote_num)
    # 1338

    # 获取用户得到感谢数
    print(author.thank_num)
    # 468

    # 获取用户关注人数
    print(author.followee_num)
    # 82

    # 获取用户关注人
    for _, followee in zip(range(0, 10), author.followees):
        print(followee.name)
    # yuwei
    # falling
    # 伍声
    # bhuztez
    # 段晓晨
    # 冯东
    # ...

    # 获取用户粉丝数
    print(author.follower_num)
    # 303

    # 获得用户粉丝
    for _, follower in zip(range(0, 10), author.followers):
        print(follower.name)
    # yuwei
    # falling
    # 周非
    # 陈泓瑾
    # O1Operator
    # ...

    # 获取用户提问数
    print(author.question_num)
    # 16

    # 获取用户所有提问的标题
    for _, question in zip(range(0, 10), author.questions):
        print(question.title)
    # 用户「松阳先生」的主页出了什么问题？
    # C++运算符重载在头文件中应该如何定义？
    # 亚马逊应用市场的应用都是正版的吗？
    # ...

    # 获取用户答题数
    print(author.answer_num)
    # 247

    # 获取用户所有回答的点赞数
    for _, answer in zip(range(0, 10), author.answers):
        print(answer.upvote_num)
    # 0
    # 5
    # 12
    # 0
    # ...

    # 获取用户文章数
    print(author.post_num)
    # 0

    # 获取用户专栏名
    for column in author.columns:
        print(column.name)
    # 我没有专栏T^T

    # 获取用户收藏夹数
    print(author.collection_num)
    # 5

    # 获取用户收藏夹名
    for collection in author.collections:
        print(collection.name)
    # 教学精品。
    # 可以留着慢慢看～
    # OwO
    # 一句。
    # Read it later

    # 获取用户动态
    for _, act in zip(range(0, 10), author.activities):
        print(act.content.url)
        if act.type == ActType.FOLLOW_COLUMN:
            print('%s 在 %s 关注了专栏 %s' %
                  (author.name, act.time, act.column.name))
        elif act.type == ActType.FOLLOW_QUESTION:
            print('%s 在 %s 关注了问题 %s' %
                  (author.name, act.time, act.question.title))
        elif act.type == ActType.ASK_QUESTION:
            print('%s 在 %s 提了个问题 %s' %
                  (author.name, act.time, act.question.title))
        elif act.type == ActType.UPVOTE_POST:
            print('%s 在 %s 赞同了专栏 %s 中 %s 的文章 %s, '
                  '此文章赞同数 %d, 评论数 %d' %
                  (author.name, act.time, act.post.column.name,
                   act.post.author.name, act.post.title, act.post.upvote_num,
                   act.post.comment_num))
        elif act.type == ActType.PUBLISH_POST:
            print('%s 在 %s 在专栏 %s 中发布了文章 %s, '
                  '此文章赞同数 %d, 评论数 %d' %
                  (author.name, act.time, act.post.column.name,
                   act.post.title, act.post.upvote_num,
                   act.post.comment_num))
        elif act.type == ActType.UPVOTE_ANSWER:
            print('%s 在 %s 赞同了问题 %s 中 %s(motto: %s) 的回答, '
                  '此回答赞同数 %d' %
                  (author.name, act.time, act.answer.question.title,
                   act.answer.author.name, act.answer.author.motto,
                   act.answer.upvote_num))
        elif act.type == ActType.ANSWER_QUESTION:
            print('%s 在 %s 回答了问题 %s 此回答赞同数 %d' %
                  (author.name, act.time, act.answer.question.title,
                   act.answer.upvote_num))
        elif act.type == ActType.FOLLOW_TOPIC:
            print('%s 在 %s 关注了话题 %s' %
                  (author.name, act.time, act.topic.name))


def test_collection():
    url = 'http://www.zhihu.com/collection/28698204'
    collection = client.collection(url)

    # 获取收藏夹名字
    print(collection.name)
    # 可以用来背的答案

    # 获取收藏夹关注人数
    print(collection.follower_num)
    # 6343

    # 获取收藏夹关注用户
    for _, follower in zip(range(0, 10), collection.followers):
        print(follower.name)
    # 花椰菜
    # 邱火羽白
    # 枫丹白露
    # ...

    # 获取收藏夹创建者名字
    print(collection.owner.name)
    # 7sDream

    # 获取收藏夹内所有答案的点赞数
    for _, answer in zip(range(0, 10), collection.answers):
        print(answer.upvote_num)
    # 2561
    # 535
    # 223
    # ...

    # 获取收藏夹内所有问题标题
    for _, question in zip(range(0, 10), collection.questions):
        print(question.title)
    # 如何完成标准的平板支撑？
    # 有没有适合 Android 开发初学者的 App 源码推荐？
    # 如何挑逗女朋友？
    # 有哪些计算机的书适合推荐给大一学生？
    # ...


def test_column():
    url = 'http://zhuanlan.zhihu.com/xiepanda'
    column = client.column(url)

    # 获取专栏名
    print(column.name)
    # 谢熊猫出没注意

    # 获取关注人数
    print(column.follower_num)
    # 73570

    # 获取文章数量
    print(column.post_num)
    # 68

    # 获取所有文章标题
    for _, post in zip(range(0, 10), column.posts):
        print(post.title)
    # 伦敦，再见。London, Pride.
    # 为什么你来到伦敦?——没有抽到h1b
    # “城邦之国”新加坡强在哪？
    # ...


def test_post():
    url = 'http://zhuanlan.zhihu.com/xiepanda/19950456'
    post = client.post(url)

    # 获取文章地址
    print(post.url)

    # 获取文章标题
    print(post.title)
    # 为什么最近有很多名人，比如比尔盖茨，马斯克、霍金等，让人们警惕人工智能？

    # 获取所在专栏名称
    print(post.column.name)
    # 谢熊猫出没注意

    # 获取作者名称
    print(post.author.name)
    # 谢熊猫君

    # 获取赞同数
    print(post.upvote_num)
    # 18491

    # 获取评论数
    print(post.comment_num)
    # 1748

    # 保存为 markdown
    post.save(filepath='.')
    # 当前目录下生成
    # 为什么最近有很多名人，比如比尔盖茨，马斯克、霍金等，让人们警惕人工智能？ - 谢熊猫君.md


def test_topic():
    url = 'http://www.zhihu.com/topic/19947695/'
    topic = client.topic(url)
    
    # 获取话题地址
    print(topic.url)
    # http://www.zhihu.com/topic/19947695/

    # 获取话题名称
    print(topic.name)
    # 深网（Deep Web）

    # 获取话题描述信息
    print(topic.description)
    # 暗网（英语：Deep Web，又称深网、不可见网、隐藏网）

    # 获取话题头像url
    print(topic.photo_url)
    # http://pic1.zhimg.com/a3b0d77c052e45399da1fe26fb4c9734_r.jpg

    # 获取话题关注人数
    print(topic.follower_num)
    # 3309

    # 获取关注者
    for _, follower in zip(range(0, 10), topic.followers):
        print(follower.name, follower.motto)
    # 韦小宝 韦小宝
    # 吉陆遥 吉陆遥
    # qingyuan ma qingyuan ma
    # ...

    # 获取父话题
    for _, parent in zip(range(0, 10), topic.parents):
        print(parent.name)
    # 互联网

    # 获取子话题
    for _, child in zip(range(0, 10), topic.children):
        print(child.name)
    # Tor

    # 获取优秀答主
    for _, author in zip(range(0, 10), topic.top_authors):
        print(author.name, author.motto)
    # Ben Chen
    # acel rovsion 我只不过规范基点上的建构论者
    # 沈万马
    # ...

    # 获取话题下的精华回答
    for _, ans in zip(range(0, 10), topic.top_answers):
        print(ans.question.title, ans.author.name, ans.upvote_num)
    # 《纸牌屋》中提到的深网 (Deep Web) 是什么？ Ben Chen 2956
    # 黑客逃避追踪，为什么要用虚拟机 + TOR + VPN 呢？ Ario 526
    # 《纸牌屋》中提到的深网 (Deep Web) 是什么？ acel rovsion 420
    # ...

    # 按时间由近到远获取所有问题
    for _, question in zip(range(0, 10), topic.questions):
        print(question.title)
    # 马里亚纳网络存在吗？
    # 玛丽亚纳网络存在吗？
    # 为什么暗网里这么多违法的东西FBI不顺藤摸瓜呢?
    # ...

    # 按时间由近到远获取所有回答
    for _, ans in zip(range(0, 10), topic.answers):
        print(ans.question.title, ans.author.name, ans.upvote_num)
    # 如何用tor登陆qq? 匿名用户 0
    # 想看一下暗网（deep web），但是怕中病毒，所以有谁能发发截图？？ tor 0
    # icq是什么 为什么暗网交流一般都用icq？ tor 0
    # ...

    # 获取话题下的热门问题，按热门度由高到低返回
    for _, q in zip(range(0, 10), topic.hot_questions):
        print(q.title)
    # 《纸牌屋》中提到的深网 (Deep Web) 是什么？
    # 黑客逃避追踪，为什么要用虚拟机 + TOR + VPN 呢？
    # 微博热传的关于暗网的变态故事是真的还是假的啊？
    # ...

    # 获取话题下的热门回答，按热门度由高到低返回
    for _, ans in zip(range(0, 10), topic.hot_answers):
        print(ans.question.title, ans.author.name, ans.upvote_num)
    # 《纸牌屋》中提到的深网 (Deep Web) 是什么？ Ben Chen 3006
    # 《纸牌屋》中提到的深网 (Deep Web) 是什么？ 提刀夜行 123
    # 《纸牌屋》中提到的深网 (Deep Web) 是什么？ 匿名用户 21
    # ...


def test_me():
    """
    本函数默认不会开启，因为函数涉及到点赞，反对，感谢，关注等主观操作

    请确认您有能力在测试代码生错误的情况下，判断出出错在哪一行，
    并将代码进行的操作回滚（即：将点赞，感谢，关注等操作取消）

    如果确认有能力，请填写代码中的空白，并将test函数中相关行注释取消
    """
    answer = client.answer('')          # 填写答案Url，不可填写自己的答案
    post = client.post('')              # 填写文章Url，不可填写自己的文章
    author = client.author('')          # 填写用户Url，不可填写自己
    question = client.question('')      # 填写问题Url
    topic = client.topic('')            # 填写话题Url
    collection = client.collection('')  # 填写收藏夹Url

    me = client.me()

    print('赞同答案...', end='')
    assert me.vote(answer, 'up')        # 赞同
    assert me.vote(answer, 'down')      # 反对
    assert me.vote(answer, 'clear')     # 清除
    print('通过')

    print('感谢答案...', end='')
    assert me.thanks(answer)            # 感谢
    assert me.thanks(answer, False)     # 取消感谢
    print('通过')

    print('赞同文章...', end='')
    assert me.vote(post, 'up')          # 赞同
    assert me.vote(post, 'down')        # 反对
    assert me.vote(post, 'clear')       # 清除
    print('通过')

    print('关注用户...', end='')
    assert me.follow(author)            # 关注
    assert me.follow(author, False)     # 取消关注
    print('通过')

    print('关注问题...', end='')
    assert me.follow(question)          # 关注
    assert me.follow(question, False)   # 取消关注
    print('通过')

    print('关注话题...', end='')
    assert me.follow(topic)             # 关注
    assert me.follow(topic, False)      # 取消关注
    print('通过')

    print('关注收藏夹...', end='')
    assert me.follow(collection)         # 关注
    assert me.follow(collection, False)  # 取消关注
    print('通过')


def test():
    test_question()
    test_answer()
    test_author()
    test_collection()
    test_column()
    test_post()
    test_topic()
    # test_me()


if __name__ == '__main__':
    Cookies_File = 'cookies.json'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    TEST_DIR = os.path.join(BASE_DIR, 'test')

    print("Test dir: ", TEST_DIR)

    if os.path.exists(TEST_DIR):
        print("Cleaning it...", end='')
        shutil.rmtree(TEST_DIR)
        print("Done")
    else:
        print("Test dir not exist.")

    os.chdir(BASE_DIR)

    if os.path.isfile(Cookies_File):
        print("Cookies file found.")
        client = ZhihuClient(Cookies_File)
    else:
        print("Cookies file not exist, please login...")
        client = ZhihuClient()
        cookies_str = client.login_in_terminal()
        with open(Cookies_File, 'w') as f:
            f.write(cookies_str)

    print("Making test dir...", end="")
    os.mkdir(TEST_DIR)
    print("Done", end="\n\n")

    os.chdir(TEST_DIR)

    print("===== test start =====")

    import timeit

    try:
        time = timeit.timeit(
            'test()', setup='from __main__ import test', number=1)
        print('===== test passed =====')
        print('no error happen')
        print('time used: {0} ms'.format(time * 1000))
    except Exception as e:
        print('===== test failed =====')
        raise e
    finally:
        os.chdir(BASE_DIR)
        print("Cleaning...", end='')
        shutil.rmtree(TEST_DIR)
        print("Done")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from .common import *
from .author import Author


class Me(Author):
    """封装了相关操作（如点赞，关注问题）的类。
    请使用 :meth:`.ZhihuClient.me` 方法获取实例。
    """

    def __init__(self, url, name, motto, photo_url, session):
        super(Me, self).__init__(url, name, motto,
                                 photo_url=photo_url, session=session)

    def vote(self, something, vote='up'):
        """给答案或文章点赞或取消点赞

        :param Answer/Post something: 需要点赞的答案或文章对象
        :param str vote:
            ===== ================ ======
            取值        说明       默认值
            ===== ================ ======
            up    赞同              √
            down  反对              X
            clear 既不赞同也不反对  X
            ===== ================ ======

        :return: 成功返回True，失败返回False
        :rtype: bool
        """
        from .answer import Answer
        from zhihu import Post
        if isinstance(something, Answer):
            mapping = {
                'up': 'vote_up',
                'clear': 'vote_neutral',
                'down': 'vote_down'
            }
            if vote not in mapping.keys():
                raise ValueError('Invalid vote value: {0}'.format(vote))
            if something.author.url == self.url:
                return False
            params = {'answer_id': str(something.aid)}
            data = {
                '_xsrf': something.xsrf,
                'method': mapping[vote],
                'params': json.dumps(params)
            }
            headers = dict(Default_Header)
            headers['Referer'] = something.question.url[:-1]
            res = self._session.post(Upvote_Answer_Url,
                                     headers=headers, data=data)
            return res.json()['r'] == 0
        elif isinstance(something, Post):
            mapping = {
                'up': 'like',
                'clear': 'none',
                'down': 'dislike'
            }
            if vote not in mapping.keys():
                raise ValueError('Invalid vote value: {0}'.format(vote))
            if something.author.url == self.url:
                return False
            put_url = Upvote_Article_Url.format(
                something.column_in_name, something.slug)
            data = {'value': mapping[vote]}
            headers = {
                'Content-Type': 'application/json;charset=utf-8',
                'Host': 'zhuanlan.zhihu.com',
                'Referer': something.url[:-1],
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                              'rv:39.0) Gecko/20100101 Firefox/39.0',
                'X-XSRF-TOKEN': self._session.cookies.get('XSRF-TOKEN')
            }
            res = self._session.put(put_url, json.dumps(data), headers=headers)
            return res.status_code == 204
        else:
            raise ValueError('argument something need to be '
                             'zhihu.Answer or zhihu.Post object.')

    def thanks(self, answer, thanks=True):
        """感谢或取消感谢回答

        :param Answer answer: 要感谢或取消感谢的回答
        :param thanks: True-->感谢，False-->取消感谢
        :return: 成功返回True，失败返回False
        :rtype: bool
        """
        from .answer import Answer
        if isinstance(answer, Answer) is False:
            raise ValueError('argument answer need to be Zhihu.Answer object.')
        if answer.author.url == self.url:
                return False
        data = {
            '_xsrf': answer.xsrf,
            'aid': answer.aid
        }
        res = self._session.post(Thanks_Url if thanks else Cancel_Thanks_Url,
                                 data=data)
        return res.json()['r'] == 0

    def follow(self, something, follow=True):
        """关注用户、问题、话题或收藏夹

        :param Author/Question/Topic something: 需要关注的对象
        :param bool follow: True-->关注，False-->取消关注
        :return: 成功返回True，失败返回False
        :rtype: bool
        """
        from .question import Question
        from .topic import Topic
        from .collection import Collection
        if isinstance(something, Author):
            if something.url == self.url:
                return False
            data = {
                '_xsrf': something.xsrf,
                'method': '	follow_member' if follow else 'unfollow_member',
                'params': json.dumps({'hash_id': something.hash_id})
            }
            res = self._session.post(Follow_Author_Url, data=data)
            return res.json()['r'] == 0
        elif isinstance(something, Question):
            data = {
                '_xsrf': something.xsrf,
                'method': 'follow_question' if follow else 'unfollow_question',
                'params': json.dumps({'question_id': str(something.qid)})
            }
            res = self._session.post(Follow_Question_Url, data=data)
            return res.json()['r'] == 0
        elif isinstance(something, Topic):
            data = {
                '_xsrf': something.xsrf,
                'method': 'follow_topic' if follow else 'unfollow_topic',
                'params': json.dumps({'topic_id': something.tid})
            }
            res = self._session.post(Follow_Topic_Url, data=data)
            return res.json()['r'] == 0
        elif isinstance(something, Collection):
            data = {
                '_xsrf': something.xsrf,
                'favlist_id': something.cid
            }
            res = self._session.post(
                Follow_Collection_Url if follow else Unfollow_Collection_Url,
                data=data)
            return res.json()['r'] == 0
        else:
            raise ValueError('argument something need to be '
                             'zhihu.Author, zhihu.Question'
                             ', Zhihu.Topic or Zhihu.Collection object.')

    def add_comment(self, answer, content):
        """给指定答案添加评论

        :param Answer answer: 答案对象
        :param string content: 评论内容
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """

        from .answer import Answer
        if isinstance(answer, Answer) is False:
            raise ValueError('argument answer need to be Zhihu.Answer object.')
        if not content:
            raise ValueError('answer content cannot be empty')
        data = {
            'method': 'add_comment',
            'params': json.dumps({'answer_id': answer.aid, 'content': content}),
            '_xsrf': answer.xsrf
            }
        res = self._session.post(Answer_Add_Comment_URL,
                                 data=data)
        return res.json()['r'] == 0

    def send_message(self, author, content):
        """发送私信给一个用户

        :param Author author: 接收私信用户对象
        :param string content: 发送给用户的私信内容
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        if isinstance(author, Author) is False:
            raise ValueError('argument answer need to be Zhihu.Author object.')
        if not content:
            raise ValueError('answer content cannot be empty')
        if author.url == self.url:
                return False
        data = {
            'member_id': author.hash_id,
            'content': content,
            'token': '',
            '_xsrf': author.xsrf
        }
        res = self._session.post(Send_Message_Url,
                                 data=data)
        return res.json()['r'] == 0

    def block(self, something, block=True):
        """屏蔽某个用户、话题

        :param Author/Topic something:
        :param block: True-->屏蔽，False-->取消屏蔽
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        from .topic import Topic

        if isinstance(something, Author):

            if something.url == self.url:
                return False
            data = {
                '_xsrf': something.xsrf,
                'action': 'add' if block else 'cancel',
            }
            block_author_url = something.url + 'block'
            res = self._session.post(block_author_url, data=data)
            return res.json()['r'] == 0
        elif isinstance(something, Topic):
            tid = something.tid
            data = {
                '_xsrf': something.xsrf,
                'method': 'add' if block else 'del',
                'tid': tid,
            }
            block_topic_url = 'http://www.zhihu.com/topic/ignore'
            res = self._session.post(block_topic_url, data=data)
            return res.status_code == 200
        else:
            raise ValueError('argument something need to be '
                             'Zhihu.Author or Zhihu.Topic object.')

    def unhelpful(self, answer, unhelpful=True):
        """没有帮助或取消没有帮助回答

        :param Answer answer: 要没有帮助或取消没有帮助回答
        :param unhelpful: True-->没有帮助，False-->取消没有帮助
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        from .answer import Answer
        if isinstance(answer, Answer) is False:
            raise ValueError('argument answer need to be Zhihu.Answer object.')
        if answer.author.url == self.url:
                return False
        data = {
            '_xsrf': answer.xsrf,
            'aid': answer.aid
        }
        res = self._session.post(Unhelpful_Url if unhelpful else Cancel_Unhelpful_Url,
                                 data=data)
        return res.json()['r'] == 0

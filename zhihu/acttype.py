#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ActType():

    """用于表示用户动态的类型.

    :常量说明:
        =============== ============== ======== ==================
        常量名          说明           提供属性 属性类型
        =============== ============== ======== ==================
        ANSWER_QUESTION 回答了一个问题 answer   :class:`.Answer`
        UPVOTE_ANSWER   赞同了一个回答 answer   :class:`.Answer`
        ASK_QUESTION    提出了一个问题 question :class:`.Question`
        FOLLOW_QUESTION 关注了一个问题 question :class:`.Question`
        UPVOTE_POST     赞同了一篇文章 post     :class:`.Post`
        FOLLOW_COLUMN   关注了一个专栏 column   :class:`.Column`
        FOLLOW_TOPIC    关注了一个话题 topic    :class:`.Topic`
        PUBLISH_POST    发表了一篇文章 post     :class:`.Post`
        =============== ============== ======== ==================

    """

    ANSWER_QUESTION = 'member_answer_question'
    UPVOTE_ANSWER = 'member_voteup_answer'
    ASK_QUESTION = 'member_ask_question'
    FOLLOW_QUESTION = 'member_follow_question'
    UPVOTE_POST = 'member_voteup_article'
    FOLLOW_COLUMN = 'member_follow_column'
    FOLLOW_TOPIC = 'member_follow_topic'
    PUBLISH_POST = 'member_create_article'

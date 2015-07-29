#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'


class Activity:

    """用户动态类，不建议手动使用，请使用Author.activities获取."""

    def __init__(self, act_type, act_time, **kwarg):
        """类对象初始化.

        :param ActType act_type: 动态类型
        :param datatime.datatime act_time: 动态发生时间
        :return: 活动对象
        :rtype: Activity
        """
        from .acttype import ActType

        if not isinstance(act_type, ActType):
            raise ValueError('invalid activity type')
        if len(kwarg) != 1:
            raise ValueError('except one kwarg (%d given)' % len(kwarg))
        self.type = act_type
        self.time = act_time
        for k, v in kwarg.items():
            self._attr = k
            setattr(self, k, v)

    @property
    def content(self):
        """获取此对象中能提供的那个属性，对应表请查看ActType类.

        :return: 对象提供的对象
        :rtype: Author or Question or Answer or Topic or Column or Post
        """
        return getattr(self, self._attr)

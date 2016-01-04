Answer 答案类
=============

..  autoclass:: zhihu.answer.Answer
    :members:
    :special-members: __init__
    .. method:: refresh()

       刷新 Answer object 的属性. 例如赞同数增加了, 先调用 ``refresh()`` 再访问 upvote_num
       属性, 可获得更新后的赞同数.

Question 问题类
===============

..  autoclass:: zhihu.question.Question
    :members:
    :special-members: __init__
    .. method:: refresh()

       刷新 Question object 的属性. 例如回答数增加了, 先调用 ``refresh()`` 再访问 answer_num
       属性, 可获得更新后的答案数量.

==========
安装和测试
==========


pip安装（推荐）
===============

.. code-block:: bash

   (sudo) pip(3) install (--upgrade) zhihu-py3

如果想同时安装lxml，获得更快的解析速度、容错率和美观程度，请开启lxml feature：

.. code-block:: bash
   
   (sudo) pip(3) install (--upgrade) zhihu-py3[lxml]


源码安装
========
依赖于beautifulsoup4、requests、html2text，会自动安装。

..  code-block:: bash

    git clone https://github.com/7sDream/zhihu-py3.git
    cd zhihu-py3
    python(3) setup.py install


测试
====

若是使用源码安装，则安装完成后可以进行一下测试

..  code-block:: bash

    cd test
    python(3) zhihu-test.py

登录方法综述：
==============

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

..  code-block:: python

    from zhihu import ZhihuClient
    client = ZhihuClient()
    client.login_in_terminal()

    # do thing you want with client

如果你的脚本不是大项目，又要多次运行，可以先按照上文方法create\_cookies，再使用：

..  code-block:: python

    from zhihu import ZhihuClient
    Cookies_File = 'cookies.json'
    client = ZhihuClient(Cookies_File)

如果项目比较大（以GUI项目为例），可以在判断出是首次使用（没有cookies文件）时，弹出登录对话框，使用get\_captcha获取验证码数据，再调用login函数手动登录并在登录成功后保存cookies文件：

..  code-block:: python

    import os
    from zhihu import ZhihuClient

    Cookies_File = 'config/cookies.json'

    client = ZhihuClient()

    def on_window_show()
        login_btn.disable()
        if os.path.isfile(Cookies_File) is False:
            captcha_imgbox.setData(client.get_captcha())
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
        code, msg, cookies = client.login(email, password, captcha)
        if code == 0:
            with open(Cookies_File, 'w') as f
                f.write(cookies)
            # turn to main window
        else:
            msgbox(msg)
            login_btn.enable()

注：以上和GUI有关的代码皆为我乱想出来的，仅作示例之用。

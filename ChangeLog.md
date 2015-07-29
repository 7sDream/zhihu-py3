# 更新日志

## 2015.07.

 - 重构项目结构
 - 增加zhihu.Client类，改善原先模块需要使用当前目录下cookies的弊端，现在的使用方法请看Readme中的示例。
 - 去掉了`_text2int`方法，因为发现知乎以K结尾的赞同数也有办法获取到准确点赞数。

## 2015.07.26

重构项目结构，转变为标准Python模块结构。

## 2015.07.26

添加`Author.photo_url`借口，用于获取用户头像。

本属性的实现较为分散，在不同的地方使用了不同的方法：

 - `Author.follower(e)s`、`Answer.upvoters`等属性返回的`Author`自带`photo_url`

 - 用户自定义的`Author`在访问过主页的情况下通过解析主页得到

 - 用户自定义的`Author`在未访问主页的情况下为了性能使用了知乎的CardProfile API

因为实现混乱所以容易有Bug，欢迎反馈。

## 2015.07.25

### 增加了获取用户关注者和粉丝的功能

`Author.followers`、`Author.folowees`，返回Author迭代器，自带url, name ,motto question_num, answer_num, upvote_num, follower_num属性。

### html解析器优选

在安装了lxml的情况下默认使用lxml作为解析器，否则使用html.parser。

### 增加答案获取点赞用户功能

`Author.upvoters`，返回Author迭代器，自带url, name ,motto question_num, answer_num, upvote_num, thank_num属性

### 增加简易判断是否为「三零用户」功能

`Author.is_zero_user()`，判断标准为，赞同，感谢，提问数，回答数均为0。

## 2015.07.23

### 各个类url属性更改为公开

暂时这样吧，有点懒了，因为这样会让使用者有机会非法修改url，可能导致Bug，以后勤快的话会改成read-only。

### 类名变更

专栏类从`Book`更名为`Cloumn`

文章类从`Article`更名为`Post`

以上两个更名同时影响了其他类的属性名，如`Author.books`变更为`Author.columns`，其他类同理。

### 接口名变更

1. 统一了一下复数的使用。比如`Author.answers_num`变为`Author.answer_num`, `Author.collections_num`变为`Author.collection_num`。也就是说某某数量的接口名为`Class.foo_num`，foo使用单数形式。

2. 知乎的赞同使用单词upvote，以前叫`agree`的地方现在都叫`upvote`。比如`Author.agree_num`变为`Author.upvote_num`, `Post.agree_num`变为`Post.upvote_num`。

3. `Answer`类的`upvote`属性更名为`upvote_num`。

### 提供`Topic`类

目前只有获取话题名的功能。

### 提供`Author.activities`

属性获取用户动态，返回`Activity`类生成器。

`Activity`类提供`type`属性用于判断动态类型，`type`为`ActType`类定义的常量，根据`type`的不同提供不同的属性，如下表：

|类型|常量|提供的成员|
|:--:|:--:|---------:|
|关注了问题|FOLLOW_QUESTION|question|
|赞同了回答|UPVOTE_ANSWER|answer|
|关注了专栏|FOLLOW_COLUMN|column|
|回答了问题|ANSWER_QUESTION|answer|
|赞同了文章|UPVOTE_POST|post|
|发布了文章|PUBLISH_POST|post|
|关注了话题|FOLLOW_TOPIC|topic|
|提了一个问题|ASK_QUESTION|question|

由于每种类型都只提供了一种属性，所以所有Activity对象都有`content`属性，用于直接获取唯一的属性。

示例代码见[zhihu-test.py][zhihu-test-py-url]的`test_author`函数最后。

`activities`属性可以在未登录（未生成cookies）的情况下使用，但是根据知乎的隐私保护政策，开启了隐私保护的用户的回答和文章，此时作者信息会是匿名用户，所以还是建议登录后使用。

## 2015.07.22

尝试修复了最新版bs4导致的问题，虽然我没明白问题在哪QuQ，求测试。

 - Windows 已测试 ([@7sDream][my-github-url])
 - Linux
    - Ubuntu 已测试([@7sDream][my-github-url])
 - Mac 已测试 ([@SimplyY][SimplyY-github-url])

## 2015.07.16

重构 Answer 和 Article 的 url 属性为 public.

## 2015.07.11:

Hotfix， 知乎更换了登录网址，做了简单的跟进，过了Test，等待Bug汇报中。

## 2015.06.04：

由[Gracker][gracker-github-url]补充了在 Ubuntu 14.04 下的测试结果，并添加了补充说明。

## 2015.05.29：

修复了当问题关注人数为0时、问题答案数为0时的崩溃问题。（感谢：[段晓晨][duan-xiao-chen-zhihu-url]）

[my-github-url]: https://github.com/7sDream
[duan-xiao-chen-zhihu-url]: http://www.zhihu.com/people/loveQt
[gracker-github-url]: https://github.com/Gracker
[SimplyY-github-url]: https://github.com/SimplyY

# 更新日志

## 2015.07.23

### 各个类url属性更改为公开

暂时这样吧，有点懒了，因为这样会让使用者有机会非法修改url，可能导致Bug，以后勤快的话会改成read-only。

### 类名变更

专栏类从`Book`更名为`Cloumn`

文章类从`Article`更名为`Post`

以上两个更名同时影响了其他类的属性名，如`Author.books`变更为`Author.columns`，其他类同理。

### 接口名变更

1. 统一了一下复数的使用。比如`Author.answers_num`变为`Author.answer_num`, `Author.collections_num`变为`Author.collection_num`。也就是说某某数量的接口名为`Class.foo_num`，foo使用单数形式。

2. 知乎的赞同使用单词upvote，以前叫`agree`的地方现在都叫`upvote`。比如`Author.agree_num`变为`Author.upvote_num`, `Post.agree_num`变为`Post.upvote_num`

3. `Answer`类的`upvote`属性更名为`upvote_num`

### 提供`Topic`类

目前只有获取话题名的功能

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
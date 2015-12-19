"""
What's this:
    | this is an Example of zhihu-py3 to analyze is user bought some fans.

Usage:
    | 1. copy your cookies file to the dir where me located
    | 2. change USER_URL at line 12 to the user's home page url.
    | 3. var FOLLOWER_CHECK_MAX_NUM defined how many newest follower will be checked.
    | 4. var ANSWER_CHECK_MAX_NUM defined how many newest answer of user will be checked.
    | 5. just run me.

Info:
    | if FOLLOWER_CHECK_MAX_NUM big than user's follower amount, it  will be auto set to user's follower amount.

Author:
    | 7sDream @ 2015.12.19.
"""

from zhihu import ZhihuClient
import datetime

# ==============================

USER_URL = "https://www.zhihu.com/people/7sdream"

FOLLOWER_CHECK_MAX_NUM = 2000
ANSWER_CHECK_MAX_NUM = 20

# ==============================


def is_zero_user(author):
    return (author.upvote_num + author.question_num + author.answer_num) <= 3


client = ZhihuClient('test.json')

user = client.author(USER_URL)

print("检查用户{user.name} at {time}".format(user=user, time=datetime.datetime.now()))

if user.follower_num < FOLLOWER_CHECK_MAX_NUM:
    FOLLOWER_CHECK_MAX_NUM = user.follower_num

print("正在检查前{FOLLOWER_CHECK_MAX_NUM}个关注者....".format(**locals()))

zeros = 0
for _, follower in zip(range(FOLLOWER_CHECK_MAX_NUM), user.followers):
    if is_zero_user(follower):
        zeros += 1

rate = zeros / FOLLOWER_CHECK_MAX_NUM
print("{user.name}最近{FOLLOWER_CHECK_MAX_NUM}个关注者中，三无用户{zeros}个，占比{rate:.2%}".format(**locals()))

print("正在检查用户答案点赞者...")

for _, ans in zip(range(ANSWER_CHECK_MAX_NUM), user.answers):
    zeros = 0
    for upvoter in ans.upvoters:
        if is_zero_user(upvoter):
            zeros += 1
    rate = zeros / ans.upvote_num if ans.upvote_num != 0 else 0
    print("在问题「{ans.question.title}」{user.name}的答案中，共有{ans.upvote_num}个点赞用户，其中三无用户{zeros}个，三无用户比率{rate:.2%}。".format(**locals()))

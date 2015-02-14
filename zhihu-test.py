__author__ = '7sDream'

from zhihu import Collection

url = 'http://www.zhihu.com/collection/37770691'
collection = Collection(url)

# 获取收藏夹名字
print(collection.name)
# 教学精品。

# 获取收藏夹关注人数
print(collection.followers_num)
# 教学精品。

# 获取收藏夹创建者
print(collection.owner)
# <zhihu.Author object at 0x03EFDB70>

# 获取收藏夹内所有答案
print(collection.answers)
# <generator object answers at 0x03F00620>

# 获取收藏夹内所有问题
print(collection.questions)
# <generator object questions at 0x03F00620>

# Author 对象 和 questions generator 用法见前文
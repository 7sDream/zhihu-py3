import unittest
import re

from zhihu.common import re_question_url


class CommonTest(unittest.TestCase):

    def test_question_url(self):
        url = 'https://www.zhihu.com/question/26901243?sort=created'
        obj = re.match(re_question_url, url)
        assert obj.group() == url

        url = 'https://www.zhihu.com/question/26901243'
        obj = re.match(re_question_url, url)
        assert obj.group() == url

        url = 'https://www.zhihu.com/question/26901243/'
        obj = re.match(re_question_url, url)
        assert obj.group() == url

        url = 'https://www.zhihu.com/question/26901243?sort=createdx'
        obj = re.match(re_question_url, url)
        assert obj is None

        url = 'https://www.zhihu.com/question/26901243sort=created'
        obj = re.match(re_question_url, url)
        assert obj is None

        url = 'https://www.zhihu.com/question/26901243/?sort=created'
        obj = re.match(re_question_url, url)
        assert obj is None

        url = 'https://www.zhihu.com/question/26901243?/sort=created'
        obj = re.match(re_question_url, url)
        assert obj is None


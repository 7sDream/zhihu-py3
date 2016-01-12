from .common import BeautifulSoup
from requests import Response
import json


class BaseZhihu:
    def _gen_soup(self, content):
        self.soup = BeautifulSoup(content)

    def _get_content(self):
        resp = self._session.get(self.url)

        if self.__class__.__name__ == 'Answer':
            if resp.history and resp.history[0].status_code in (301, 302):
                self._deleted = True
            else:
                self._deleted = False

        return resp.content

    def _make_soup(self):
        if self.url and not self.soup:
            self._gen_soup(self._get_content())

    def refresh(self):
        # refresh self.soup's content
        self._gen_soup(self._get_content())

    @classmethod
    def from_html(cls, content):
        obj = cls(url=None)
        obj._gen_soup(content)
        return obj


class JsonAsSoupMixin:
    def _gen_soup(self, content):
        # 为了让`from_html`对外提供统一的接口, 判断一下输入, 如果是bytes 或者 str 则用json处理,
        # 否则认为是由_get_content返回的dict

        if isinstance(content, bytes):
            r = Response()
            r._content = content
            soup = r.json()
            self.soup = soup
        elif isinstance(content, str):
            self.soup = json.loads(content)
        else:
            self.soup = content

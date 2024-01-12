from html.parser import HTMLParser
from urllib import parse

from django.core.exceptions import ValidationError


__all__ = ["YTIframeParser", "YaMapScriptParser"]


class SimpleTagParser(HTMLParser):
    query_splitter = '&'
    tagname: str
    constants = {}
    required_attrs = ()

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.has_starttag = False
        self.has_endtag = False
        self.attrs = {}
        self.has_other_tags = False

    def set_attr(self, name, value):
        self.attrs[name] = value

    def process_attrs(self):
        self.attrs.update(self.constants)

    def handle_starttag(self, tag, attrs):
        if tag == self.tagname and not self.has_starttag:
            self.has_starttag = True
            for attr in attrs:
                self.set_attr(*attr)
            self.process_attrs()
        else:
            self.has_other_tags = True

    def handle_endtag(self, tag):
        if tag == self.tagname and not self.has_endtag:
            self.has_endtag = True
        else:
            self.has_other_tags = True

    def is_valid(self):
        return (
                self.has_starttag and self.has_endtag and not self.has_other_tags
                and all(attr in self.attrs for attr in self.required_attrs)
        )

    def build(self):
        return (
            f"<{self.tagname} "
            f"{" ".join(attr if value is None else f'{attr}="{value}"' for attr, value in self.attrs.items())}>"
            f"</{self.tagname}>"
        )

    def set_default_query_params(self, url_string, defaults, required: bool = False):
        url = parse.urlparse(url_string)
        query = {(kv := q.split('='))[0]: kv[1] for q in url.query.split('&')}
        if required:
            for k, v in defaults.items():
                query[k] = v
        else:
            for k, v in defaults.items():
                query.setdefault(k, v)
        qs = self.query_splitter.join(k if v is None else f"{k}={v}" for k, v in query.items())
        return parse.ParseResult(**{**url._asdict(), 'query': qs}).geturl()

    @classmethod
    def validate(cls, value):
        if not value:
            return
        parser = cls()
        parser.feed(value)
        if not parser.is_valid():
            raise ValidationError('Неверный формат')

    @classmethod
    def transform(cls, value):
        if not value:
            return ''
        parser = cls()
        parser.feed(value)
        assert parser.is_valid()
        return parser.build()


class YTIframeParser(SimpleTagParser):
    tagname = 'iframe'
    constants = {'width': '560', 'height': '315'}
    required_attrs = ('width', 'height', 'src', 'allow')

    def set_attr(self, name, value):
        if name == 'src':
            value = self.set_default_query_params(value, {'enablejsapi': '1'})
        elif name == 'allow':
            allows = [a.strip() for a in value.split(';')]
            if 'picture-in-picture' in allows:
                allows.remove('picture-in-picture')
            value = '; '.join(allows)
        super().set_attr(name, value)


class YaMapScriptParser(SimpleTagParser):
    tagname = 'script'
    query_splitter = '&amp;'
    required_attrs = ('src', 'type')

    def set_attr(self, name, value):
        if name == 'src':
            value = self.set_default_query_params(value, {'width': '100%25', 'height': '400'}, required=True)
            print(value)
        super().set_attr(name, value)

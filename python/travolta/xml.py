from lxml.etree import iterparse

class XmlInputStream():
    def __init__(self, xmlf, params):
        self.xmlf = xmlf
        self.tag = params['tag']
        self.iter = iterparse(self.xmlf, tag=self.tag)

    def __iter__(self):
        return self

    def next(self):
        t = self.iter.next()
        if t:
            return t[1].text

    def read(self, num_bytes=None):
        pass

def xml_input_stream(stream, size, url, params):
    from travolta.xml import XmlInputStream

    return XmlInputStream(url, params)

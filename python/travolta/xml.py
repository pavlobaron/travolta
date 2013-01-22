from lxml.etree import iterparse

class XmlInputStream(object):
    def __init__(self, xmlf, params):
        self.xmlf = xmlf
        if params.has_key('tag'):
            self.tag = "/}%s" % params['tag']
        else:
            self.tag = None

        self.iter = iterparse(self.xmlf)

    def __iter__(self):
        return self

    def next(self):
        while True:
            t = self.iter.next()
            if t and t[0] == 'end':
                if self.tag:
                    if t[1].tag.endswith(self.tag):
                        return t[1].text
                else:
                    return t[1].text

    def read(self, num_bytes=None):
        pass

def xml_input_stream(stream, size, url, params):
    from travolta.xml import XmlInputStream

    return XmlInputStream(url, params)

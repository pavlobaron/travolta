from travolta.xml import XmlInputStream
import re

class WikiInputStream(XmlInputStream):
    def __init__(self, xmlf, params):
        super(WikiInputStream, self).__init__(xmlf, params)
        self.patterns = [
            [re.compile("\*+", re.M), ""], #asterisks
            [re.compile("'+", re.M), ""], #font format
            [re.compile(":\s", re.M), ""], #indentations
            [re.compile("#\s", re.M), ""], #numbered lists

            [re.compile("<[^<>]+?>", re.M), " "], #any xml/html tags
            [re.compile("<[^<>]+?>", re.M), " "], #any xml/html tags (nested)
            [re.compile("{{[^{}]*?}}", re.M), ""], #anything within {{}}
            [re.compile("{{[^{}]*?}}", re.M), ""], #anything within {{}} (nested)
            [re.compile("=+\s*(See also|External links|References|Other representations)\s*=+", re.M), ""], #noise headings
            [re.compile("#REDIRECT\s+\[\[.*?\]\]", re.M), ""], #redirects
            [re.compile("http://[\w/.\-]+", re.M), ""], #http references
            [re.compile("\[\[[^\[\]]*?\|\s*([^\|\[]*?)\s*\]\]", re.M), r"\1"], #internal links
            [re.compile("\[\[[^\[\]]+?\]\]", re.M), ""], #anything within [[]]
            [re.compile("\[\[[^\[\]]+?\]\]", re.M), ""], #anything within [[]] (nested)
            [re.compile("\[[^\[\]]+?\]", re.M), ""], #anything within []

            #table
            [re.compile("{\|[^\n]*?\n", re.M), ""], #start
            [re.compile("\|}", re.M), ""], #end
            [re.compile("\|\+([^\n]*)\n", re.M), r"\1"], #caption
            [re.compile("\|-[^\n]*\n", re.M), "\n"], #splitter
            [re.compile("([^!])!([^!]*)!!", re.M), r"\1!\n\2!"], #headers reformat
            [re.compile("!\s*([^!\n]+)\n", re.M), r"\1\n"], #headers (multi liner)
            [re.compile("([^\|])\|([^\|]*)\|\|", re.M), r"\1\|\n\2\|"], #row reformat
            [re.compile("\|\s*([^\|\n]*)\n", re.M), r"\1\n"], #row (multi liner)

            [re.compile("{[^{}]*?}", re.M), ""], #anything within {}
            [re.compile("----", re.M), ""], #rule
            [re.compile("=+\s*(.+?)\s*=+", re.M), r"\n\1\n"], #headings
            [re.compile("&[^;\s]+?;", re.M), " "], #html special chars

            [re.compile("\s*\(\s*\)\s*", re.M), " "], #rest noise
            [re.compile("\s*\[\s*\]\s*", re.M), " "], #rest noise
            [re.compile("(\s*,\s*)+", re.M), ", "], #rest noise
            [re.compile("(\s*\.\s*)+", re.M), ". "], #rest noise
            [re.compile("\s*\|\s*", re.M), ""], #rest noise
            [re.compile("\n\n+", re.M), "\n"], #multi LF
            [re.compile("\s\s+", re.M), " "] #multi spaces
        ]

    def __iter__(self):
        return self

    def next(self):
        t = super(WikiInputStream, self).next()
        c = str(re.findall(re.compile("\[\[Category:(.*?)\]\]"), t))
        r = self.filter_markup(t)
        
        return "%s|||||%s" % (c, r)

    def read(self, num_bytes=None):
        pass

    def filter_markup(self, text):
        ret = text
        for a in self.patterns:
            ret = re.sub(a[0], a[1], ret)

        ret = ret.strip()
        if len(ret) == 0:
            return None

        return ret

def wiki_input_stream(stream, size, url, params):
    from travolta.wiki import WikiInputStream

    return WikiInputStream(url, params)

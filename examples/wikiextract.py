from disco.core import Job, result_iterator
from travolta.wiki import wiki_input_stream

def map(tin, params):
    if tin:
        l = tin.split("|||||")
        text = l[1]
        cat = l[0]
        if text != "None":
            yield text, cat

if __name__ == '__main__':
    job = Job().run(input =
                    ["/Users/pb/code/travolta/examples/data/wikiextract.xml"],
                    map = map,
                    map_input_stream = [wiki_input_stream],
                    required_modules = [('travolta.wiki', '/Users/pb/code/travolta/python')],
                    params = {"tag": "text"})
    for text, _cat in result_iterator(job.wait(show=True)):
        print text

from disco.core import Job, result_iterator
from travolta.xml import xml_input_stream

def map(book, params):
    yield book, None

if __name__ == '__main__':
    job = Job().run(input = ["/Users/pb/code/travolta/examples/data/books.xml"],
                    map = map,
                    map_input_stream = [xml_input_stream],
                    required_modules = [('travolta.xml', '/Users/pb/code/travolta/python')],
                    params = {'tag': 'title'})
    for book, _dummy in result_iterator(job.wait(show=True)):
        print book

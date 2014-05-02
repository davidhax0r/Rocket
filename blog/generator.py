__author__ = 'naumanahmad'
from flask import Flask,render_template
import markdown,os,yaml
from werkzeug.utils import cached_property

#Constants Defined
FILE_EXTENSION = '.md'

app = Flask(__name__)
app.secret_key = 'f8ssdf00sas#$2233500966*@!'

class Post(object):

    def __init__(self,path):
        self.path = path
        self._init_metadata()

    @cached_property
    def html(self):
        """
        Convert markdown into HTML for displaying on the template
        @cached_property - a part of the werkzeug module - caches the property
        """
        with open(self.path,'r') as file_input:
            content = file_input.read().split('\n\n',1)[1].strip()
            return markdown.markdown(content)

    def _init_metadata(self):
        """
        Loads the meta-data from the blog post file and loads in into the class dictionary
        """
        content = ''
        with open(self.path,'r') as file_input:
            for each_line in file_input:
                if not each_line.strip():
                    break
                content += each_line
            self.__dict__.update(yaml.load(content))

def format_date(value,format = '%B %d, %Y'):
    return value.strftime(format)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/blog/<path:path>')
def post(path):
    path = os.path.join('posts', path + FILE_EXTENSION)
    post = Post(path)
    return render_template('post.html',post = post, format_date = format_date)

if __name__ == '__main__':
    app.run(debug=True)
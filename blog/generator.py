"""
Copyright 2014 Nauman Ahmad

This file is part of the Rocket library.

Rocket is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

Rocket is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Rocket.
If not, see http://www.gnu.org/licenses/.
"""

from flask import Flask,render_template
import markdown,os,yaml
from werkzeug.utils import cached_property

#Constants Defined
FILE_EXTENSION = '.md'

app = Flask(__name__)
app.secret_key = 'f8ssdf00sas#$2233500966*@!'

class Post(object):

    def __init__(self,path):
        """
        The *path* param takes in the path of the blog post
        The _init_metadata() method is also called to store all the meta-data attributes into the class's __dict__
        """
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
    """
    This functions turns the date from the set meta-data format into a different format
    The *format* param can be changed to change the format of the generated date
    """
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
import web
import os
import os.path
import uuid

class Index(object):
    def GET(self):
        return '<html><body><h1>Hello World</h1></body></html>'

class Publish(object):
    def GET(self):
        raise web.seeother('/')

    def POST(self):
        form = web.input()
        web.debug(','.join(form.keys()))

publish_dir = 'publish'
urls = ('/', 'Index',
        '/publish', 'Publish')
app = web.application(urls, globals())


def setup_env():
    if not os.path.exists(publish_dir):
        os.mkdir(publish_dir)

setup_env()

if __name__ == '__main__':
    setup_env()
    app.run()

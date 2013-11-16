import web

class Index(object):
    def GET(self):
        return '<html><body><h1>Hello World</h1></body></html>'

urls = ('/.*', 'Index')
app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()

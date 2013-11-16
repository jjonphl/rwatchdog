import web
import os
import os.path
import json

import uuid
import dbutil
import rutil

publish_dir = 'publish'
db = dbutil.DatabaseUtil()
r  = rutil.RUtil()

class Index(object):
    def GET(self):
        return '<html><body><h1>Hello World</h1></body></html>'

class Publish(object):
    def GET(self):
        raise web.seeother('/')

    def _validate(self, form):
        '''
        Returns tuple (error, error_msg). error is True if there is an error.
        '''
        if not 'md_file' in form:
            return (True, 'Missing md_file parameter.')

        return (False,None)


    def _save_file(self, path, file_param, filename=None):
        _path = os.path.join(path, filename if filename else file_param.filename)
        _file = open(_path, 'wb')
        _file.write(file_param.value)

    def _save(self, form):
        _uuid = str(uuid.uuid4())
        while os.path.exists(os.path.join(publish_dir, _uuid)):
            _uuid = str(uuid.uuid4())   # prob this happens ~ 0

        # create directory
        _path = os.path.join(publish_dir, _uuid, 'upload')
        os.mkdir(_path)

        # save md_file
        self._save_file(_path, form['md_file'])

        # save data_file[] if it/they exist(s)
        if 'data_file' in form:
            # special handling for "param array"
            file_param = web.webapi.rawinput().get('data_file')
            if not isinstance(file_param, list):
                file_param = list(file_param)
            for f in file_param:
                self._save_file(_path, f)

        # save rdata_file if it exists
        if form['rdata_file'] != {}:
            self._save_file(_path, form['rdata_file'], 'data.rda')

        # save to database
        db.save(_uuid, form['md_file'].filename)

        return (False, None, _uuid)


    def POST(self):
        form = web.input(md_file={}, data_file={}, rdata_file={})
        (error, error_msg) = self._validate(form)

        if not error:
            (error, error_msg, uuid) = self._save(form)

        if error:
            ret = {'status': 'error', 'message': error_msg}
        else:
            ret = {'status': 'ok', 'uuid': uuid}

        return json.dumps(ret)

class Status(object):
    def GET(self):
        pass

class View(object):
    def GET(self):
        pass

urls = ('/', 'Index',
        '/publish', 'Publish',   # publish new .Rmd file
        '/status', 'Status',     # query publishing status
        '/view', 'View')         # view published .Rmd

app = web.application(urls, globals())


def setup_env():
    # setup publish directory
    if not os.path.exists(publish_dir):
        os.mkdir(publish_dir)

    db.setup()
    r.setup()



setup_env()

if __name__ == '__main__':
    setup_env()
    app.run()

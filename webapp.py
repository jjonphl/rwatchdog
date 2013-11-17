import web
import os
import os.path
import json
import ConfigParser 
import sys

import uuid
import dbutil
import rutil

config = ConfigParser.ConfigParser()
config.read('webapp.conf')

publish_path = config.get('webapp', 'publish_path')
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
        error, error_msg = None, None

        _uuid = str(uuid.uuid4())
        while os.path.exists(os.path.join(publish_path, _uuid)):
            _uuid = str(uuid.uuid4())   # prob this happens ~ 0

        # create directory
        _path = os.path.join(publish_path, _uuid, 'upload')
        os.makedirs(_path)

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
        try:
            db.save(_uuid, form['md_file'].filename)
        except:
            error = True
            error_msg = str(sys.exc_info()[1])

        if not error:
            try:
                rutil.knit_spawn(_uuid)
                print 'spawned...'
            except:
                error = True
                error_msg = str(sys.exc_info()[1])

        return (error, error_msg, _uuid)


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
        form = web.input()
        uuid = form['uuid']
        (status, message) = db.get_status(uuid)
        ret = {'uuid': uuid, 'status': status, 'message': message}
        return json.dumps(ret)

class View(object):
    def GET(self):
        form = web.input()
        uuid = form['uuid']

        if not uuid:
            raise StandardError('Please specify uuid.')

        md = db.get_md_file(uuid)
        md = os.path.splitext(md)[0]
        raise web.seeother('/%s/%s/upload/%s.html' % (publish_path, uuid, md))

urls = ('/', 'Index',
        '/publish', 'Publish',   # publish new .Rmd file
        '/status', 'Status',     # query publishing status
        '/view', 'View')         # view published .Rmd

app = web.application(urls, globals())


def setup_env():
    # setup publish directory
    if not os.path.exists(publish_path):
        os.mkdir(publish_path)

    db.setup()
    r.setup()



setup_env()

if __name__ == '__main__':
    setup_env()
    app.run()

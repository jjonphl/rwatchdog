import subprocess as sp
import sys
import os
import os.path
import glob
import ConfigParser 
import time
import StringIO

import dbutil

_unix = False

class RUtil(object):

    def __init__(self, arch='x64', config='webapp.conf'):
        self._arch = arch

        conf = ConfigParser.ConfigParser()
        conf.read(config)
        self._publish_path = conf.get('webapp', 'publish_path')

    def setup(self):
        # check that R is available
        try:
            sp.call(['Rscript', '--arch', self._arch, '--version'])
        except OSError, e:
            raise StandardError('Rscript not found: %s' % (e.strerror,))

        # check that knitr is available
        ret = sp.call(['Rscript', '--arch', self._arch, '-e', 'library(knitr)'])
        if ret != 0:
            raise StandardError('R library knitr not found.')

    def knitr(self, uuid, db):
        cmd = ['Rscript', '--arch', self._arch, '-e']
        if _unix:
            cmd.append('source("__compile__.R")')
        else:
            cmd.append('"source(\'__compile__.R\')"')

        path = os.path.join(self._publish_path, uuid)

        if not os.path.isdir(path):
            raise StandardError('Invalid publish path: %s' % (path,))

        ipath = os.path.join(path, 'upload')
        if not os.path.isdir(ipath):
            raise StandardError('No uploaded files for %s.' % (uuid,))

        script = open(os.path.join(ipath, '__compile__.R'), 'w')
        script.write('library(knitr)\n')

        # test if there is an R data file (data.rda)
        rda_path = os.path.join(ipath, 'data.rda')
        if os.path.exists(rda_path):
            script.write('load("data.rda")')

        # get .Rmd file
        if db:
            md_file = db.get_md_file(uuid)
        else:
            try:
                md_file = glob.iglob(os.path.join(ipath, '*.Rmd')).next()
            except StopIteration:
                raise StandardError('No Rmd file uploaded.')

            md_file = os.path.split(md_file)[1]

        script.write('knit2html("%s", options=c("use_xhtml", "smartypants", "mathjax", "highlight_code"))\n' % (md_file,))
        script.close()

        if db:
            db.update_status(uuid, 'starting', None)

        try:
            proc = sp.Popen(cmd, cwd=ipath, stderr=sp.PIPE, shell=True)
            buf = StringIO.StringIO()
            ret = proc.poll()

            while ret is None:
                buf.write(proc.stderr.read())
                print 'BUF: %s' % (buf.getvalue(),)
                if db:
                    db.update_status(uuid, 'running', buf.getvalue())
                time.sleep(1)
                ret = proc.poll()

            buf.write(proc.stderr.read())
            if db:
                db.update_status(uuid, 'running', buf.getvalue())

            if ret == 0:
                print 'knit successful'
                if db:
                    db.update_status(uuid, 'finished', None)
            else:
                if db:
                    db.update_status(uuid, 'error', 'Returned: %d' % (ret,))
                else:
                    print 'Error: %d' % (ret,)

        except OSError, e:
            if db:
                db.update_status(uuid, 'error', e.strerror)
            else:
                print e.strerror
        except:
            error = str(sys.exc_info()[1])
            if db:
                db.update_status(uuid, 'error', error)
            else:
                print error
              


def knit_spawn(uuid):
    sp.call(['python', 'rutil.py', uuid])

if __name__ == '__main__':
    uuid = sys.argv[1]

    db = dbutil.DatabaseUtil()
    r = RUtil()
    r.knitr(uuid, db)




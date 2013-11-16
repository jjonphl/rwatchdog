import subprocess as sp
import sys
import os
import os.path
import glob
import ConfigParser 
import time
import StringIO

import dbutil

class RUtil(object):

    def __init__(self, arch='x64', config='webapp.conf'):
        self._arch = arch

        conf = ConfigParser.ConfigParser()
        conf.read(config)
        self._publish_path = config.get('webapp', 'publish_path')

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
        cmd = ['Rscript', '--arch', self._arch]
        path = os.path.join(self._publish_path, uuid)

        if not os.path.isdir(path):
            raise StandardError('Invalid publish path: %s' % (path,))

        ipath = os.path.join(path, 'upload')
        if not os.path.isdir(ipath):
            raise StandardError('No uploaded files for %s.' % (uuid,))

        opath = os.path.join(path, 'output')
        if not os.path.exists(opath):
            os.mkdir(opath)

        cmd.append('-e')
        cmd.append('library(knitr)')

        # test if there is an R data file (data.rda)
        rda_path = os.path.join(ipath, 'data.rda')
        if os.path.exists(rda_path):
            cmd.append('-e')
            cmd.append('load("../upload/data.rda")')

        # get .Rmd file
        if db:
            md_file = db.get_md_file(uuid)
        else:
            try:
                md_file = glob.iglob(os.path.join(ipath, '*.Rmd')).next()
            except StopIteration:
                raise StandardError('No Rmd file uploaded.')

            md_file = os.path.split(md_file)[1]

        cmd.append('-e')
        cmd.append('knit2html("../upload/%s", options=c("use_xhtml", "smartypants", "mathjax", "highlight_code"))')

        if db:
            db.update_status(uuid, 'starting', None)

        try:
            proc = sp.Popen(cmd, cwd=opath, stdout=sp.PIPE)
            buf = StringIO.StringIO()

            while proc.poll() is None:
                buf.write(proc.read())
                if db:
                    db.update_status(uuid, 'running', buf.getvalue())
                time.sleep(1)
         except OSError, e:
            if db:
                db.update_status(uuid, 'error', e.strerror)
            else:
                print e.strerror
         except:
             error = sys.exc_info()[0]
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




import sqlite3
import ConfigParser 

conf = ConfigParser.ConfigParser()
conf.read('webapp.conf')

class _SQLiteDatabaseUtil(object):
    def __init__(self, config='webapp.conf'):
        conf = ConfigParser.ConfigParser()
        conf.read(config)
        filename = conf.get('sqlite3', 'filename')
        self._db = sqlite3.connect(filename)

    def setup(self):
        cu = self._db.cursor()
        cu.execute('SELECT 1 FROM sqlite_master WHERE name=? AND type=?',
                ('publications', 'table'))
        if not cu.fetchone():
            cu.execute('''
CREATE TABLE publications(
    uuid       CHAR(40) NOT NULL,
    md_file    VARCHAR(255) NOT NULL, 
    status     CHAR(10) NOT NULL,
    message    TEXT,
    CONSTRAINT pk_publications PRIMARY KEY(uuid))''')

    def save(self, uuid, md_file, status='created', message=''):
        cu = self._db.cursor()
        cu.execute('''
INSERT INTO publications(uuid, md_file, status, message)
VALUES(?, ?, ?, ?)''', (uuid, md_file, status, message))
        self._db.commit()

    def get_md_file(self, uuid):
        cu = self._db.cursor()
        cu.execute('''
SELECT md_file
  FROM publications
 WHERE uuid = ?''', (uuid,))
        ret = cu.fetchone()
        self._db.commit()
        return ret[0] if ret else None

    def get_status(self, uuid):
        cu = self._db.cursor()
        cu.execute('''
SELECT status, message
  FROM publications
 WHERE uuid = ?''', (uuid,))
        ret = cu.fetchone()
        self._db.commit()
        return (ret[0], ret[1]) if ret else None

    def update_status(self, uuid, status, message):
        cu = self._db.cursor()
        cu.execute('''
UPDATE publications
   SET status = ?,
       message = ?
 WHERE uuid = ?''', (status, message, uuid))
        self._db.commit()

DatabaseUtil = _SQLiteDatabaseUtil

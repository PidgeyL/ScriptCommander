import os
import sqlite3


from scriptcommander.settings import database_file, config_dir
from scriptcommander.database import db_creation_statements

class Database():
    def __init__(self):
        self.db_file = database_file
        pass

    def _connection(self):
        # Make config dir if not exists
        os.makedirs(config_dir, mode=0o740, exist_ok=True)
        # Connect database & make sure the structure exists
        conn = sqlite3.connect( self.db_file )
        for i in db_creation_statements:
            conn.execute( i )
        return conn


    def committing(funct):
        def wrapper(self, *args, **kwargs):
            try:
                conn = self._connection()
                cur  = conn.cursor()
                funct(self, cur, *args, **kwargs)
            except Exception as e:
                conn.rollback()
                raise(e)
            else:
                conn.commit()
        return wrapper


    def getting(funct):
        def wrapper(self, *args, **kwargs):
            conn  = self._connection()
            cur   = conn.cursor()
            data  = funct(self, cur, *args, **kwargs)
            names = list(map(lambda x: x[0], cur.description))
            ndata = []
            if not data:
                return []
            for entry in data:
                j = {}
                for i in range(0,len(names)):
                    j[names[i].lower()] = entry[i]
                ndata.append(j)
            return ndata
        return wrapper

    # Scripts
    @getting
    def get_scripts(self, cur):
        return cur.execute("""SELECT *
                              FROM scripts;""")

    @committing
    def add_script(self, cur, name, _file, version, hash, enabled):
        cur.execute("""INSERT INTO scripts(script_name, script_file, script_version,
                                           script_hash, enabled)
                               VALUES(?, ?, ?, ?, ?);""", (name, _file, version, hash, enabled))

    @committing
    def update_script(self, cur, name, _file, version, hash, last_run, enabled):
        cur.execute("""UPDATE scripts
                           SET script_name = ?, script_file = ?, script_version = ?,
                               script_hash = ?, last_run = ?, enabled = ?
                       WHERE script_hash = ?;""",
                    (name, _file, version, hash, last_run, enabled, hash))

    @committing
    def delete_script(self, cur, hash):
        cur.execute("""DELETE FROM scripts
                       WHERE script_hash = ?;""", (hash,))

    # Settings
    @committing
    def set_setting(self, cur, name, value):
        cur.execute("""INSERT OR REPLACE INTO settings(name, value)
                       VALUES(?, ?);""", (name, value))

    @committing
    def del_setting(self, cur, name):
        cur.execute("""DELETE FROM settings
                       WHERE name = ?;""", (name,))

    @getting
    def get_setting(self, cur, name):
        return cur.execute("""SELECT value
                              FROM settings
                              WHERE name = ?""", (name, ))

    @getting
    def list_settings(self, cur):
        return cur.execute("""SELECT name
                              FROM settings;""")

    # Logs
    @committing
    def add_log(self, cur, script_hash, log_time, level, text):
        cur.execute("""INSERT INTO logs(script_hash, alert_time, level, text)
                       VALUES(?, ?, ?, ?)""", (script_hash, log_time, level, text))

    @getting
    def get_all_logs(self, cur):
        return cur.execute("""SELECT *
                              FROM logs;""")

    @getting
    def get_all_logs_for_level(self, cur, log_level):
        return cur.execute("""SELECT *
                              FROM logs
                              WHERE level >= ?;""", (log_level,))

    @getting
    def get_logs_for_script(self, cur, hash, log_level):
        return cur.execute("""SELECT *
                              FROM logs
                              WHERE script_hash = ?
                                AND level >= ?;""", (hash, log_level))

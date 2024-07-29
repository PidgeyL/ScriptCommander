_TABLE_SCRIPTS_ = '''
    CREATE TABLE IF NOT EXISTS scripts(
        script_name       TEXT        NOT NULL,
        script_file       TEXT        NOT NULL,
        script_version    TEXT        NOT NULL,
        script_hash       TEXT        PRIMARY KEY  NOT NULL,
        last_run          DATETIME,
        enabled           BOOLEAN     NOT NULL
    );'''

_TABLE_LOGS_ = '''
    CREATE TABLE IF NOT EXISTS logs(
        id            INTEGER    PRIMARY KEY  AUTOINCREMENT,
        script_hash   INTEGER    NOT NULL,
        alert_time    DATETIME   NOT NULL,
        level         INTEGER    NOT NULL,
        text          TEXT       NOT NULL
    );'''

_TABLE_SETTINGS_ = '''
    CREATE TABLE IF NOT EXISTS settings(
        name     TEXT    PRIMARY KEY,
        value    TEXT    NOT NULL
    );'''


db_creation_statements = [_TABLE_SCRIPTS_, _TABLE_LOGS_, _TABLE_SETTINGS_]

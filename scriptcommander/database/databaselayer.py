from datetime import datetime

from scriptcommander.database  import Database
from scriptcommander.tools     import Singleton

_LOG_LEVELS_          = {'debug': 1, 'info': 2, 'warning': 3, 'error': 4, 'critical': 5}
_LOG_LEVELS_REVERSED_ = {v: k for k, v in _LOG_LEVELS_.items()}


class DatabaseLayer(metaclass=Singleton):
    def __init__(self):
        self.db = Database()


    # Scripts
    def get_scripts(self):
        data = self.db.get_scripts()
        for entry in data:
            entry['enabled'] = bool(entry['enabled'])
        return data

    def add_script(self, script):
        self.db.add_script(script['script_name'], script['script_file'], script['script_version'],
                           script['script_hash'], script['enabled'] )

    def set_script_status(self, script, status):
        self.db.update_script(script['script_name'], script['script_file'], script['script_version'],
                              script['script_hash'], script['last_run'], status)

    def delete_script(self, script):
        self.db.delete_script(script['script_hash'])


    # Settings
    def set_setting(self, setting, value):
        self.db.set_setting(setting, value)

    def del_setting(self, setting):
        self.db.del_setting(setting)

    def get_setting(self, setting):
        data = self.db.get_setting(setting)
        if data:
            return data[0]['value']
        return None

    def list_settings(self):
        return [x['name'] for x in self.db.list_settings()] or []


    # Logs
    def add_log(self, script_hash, level, text):
        now = datetime.now()
        if isinstance(level, str):
            level = _LOG_LEVELS_.get(level.lower(), 0)
        self.db.add_log(script_hash, now, level, text)

    def get_logs(self, script_hash=None, level=None):
        # Check if we use the log level names
        if isinstance(level, str):
            level = _LOG_LEVELS_.get(level.lower(), None)
        # Check if we ended up with a valid int
        if (not isinstance(level, int)
           or (level > max(_LOG_LEVELS_.values()) and
               level < min(_LOG_LEVELS_.values()))):
             # If not a valid level, use the lowest
            level = min(_LOG_LEVELS_.values())
        if script_hash:
            logs = self.db.get_logs_for_script(script_hash, level)
        else:
            logs = self.db.get_all_logs_for_level(level)
        for log in logs:
            log['level'] = _LOG_LEVELS_REVERSED_[log['level']]
        return logs

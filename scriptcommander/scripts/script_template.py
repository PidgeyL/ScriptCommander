from scriptcommander.database import DatabaseLayer
from scriptcommander.logging  import ScriptLogger

class Script():
    name     = "Example Script"
    version  = "0.1"
    settings = []
    hash     = "NotSet"

    def __init__(self):
        pass


    def validate_settings(self):
        missing = []
        dbl     = DatabaseLayer()
        for setting in self.settings:
            if not dbl.get_setting(setting):
                missing.append(setting)
        if missing:
            return missing
        return True


    def debug(self, message):
        ScriptLogger().debug(self.hash, message, name=f"{self.name} ({self.version})")

    def info(self, message):
        ScriptLogger().info(self.hash, message, name=f"{self.name} ({self.version})")

    def warn(self, message):
        ScriptLogger().warn(self.hash, message, name=f"{self.name} ({self.version})")

    def error(self, message):
        ScriptLogger().error(self.hash, message, name=f"{self.name} ({self.version})")

    def critical(self, message):
        ScriptLogger().critical(self.hash, message, name=f"{self.name} ({self.version})")


    def run(self):
        self.critical("Fuction 'run' not implemented.")
        pass

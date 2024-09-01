import hashlib
import importlib
import os
import sys


from scriptcommander.database import DatabaseLayer
from scriptcommander.logging  import ScriptLogger
from scriptcommander.settings import script_dir
from scriptcommander.tools    import Singleton
# Long name to avoid circular import with __init__.py
from scriptcommander.scripts.script_template  import Script


class ScriptManager(metaclass=Singleton):
    def __init__(self):
        self.dbl        = DatabaseLayer()
        self.script_dir = script_dir
        self.logger     = ScriptLogger()
        # Make config dir if not exists
        os.makedirs(script_dir, mode=0o740, exist_ok=True)


    def _load_script(self, _path):
        script_spec = importlib.util.spec_from_file_location("Script", _path)
        script_file = importlib.util.module_from_spec(script_spec)
        script_spec.loader.exec_module(script_file)
        script      = script_file.Script()
        script.hash = hashlib.shake_256(open(_path, 'rb').read()).hexdigest(4)
        script.path = _path
        return script


    def scan_scripts(self):
        scripts = []
        for root, dirs, files in os.walk( self.script_dir ):
            for _file in [f for f in files if f.endswith(".py")]:
                _path = os.path.join(root, _file) # Full path
                path  = _path.removeprefix(self.script_dir + "/")
                # test if this is a valid script
                try:
                    script = self._load_script(_path)
                    assert isinstance(script, Script)
                    entry = {}
                    entry['script_name']    = script.name
                    entry['script_version'] = script.version
                    entry['script_file']    = path
                    entry['script_hash']    = hashlib.shake_256(open(_path, 'rb').read()).hexdigest(4)
                    scripts.append(entry)
                except AttributeError as e:
                    if "has no attribute 'Script'" in str(e):
                        pass
                    else:
                        print(e)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(e)
                    print(type(e))
                    pass
        return scripts


    def get_active_scripts(self):
        scripts = []
        for _script in [s for s in self.dbl.get_scripts() if s['enabled']]:
            script = self._load_script( os.path.join(self.script_dir, _script['script_file']) )
            if script.hash != _script['script_hash']:
                self.logger.critical(_script['script_hash'],
                                     f"The hash changed for {_script['script_file']}",
                                     name=f"{_script['script_name']} ({_script['script_version']})")
            else:
                scripts.append(script)
        return scripts


    def run_scripts(self):
        for script in self.get_active_scripts():
            script_name = f"{script.name} ({script.version})"

            settings    = script.validate_settings()
            if settings == True:
                try:
                    self.logger.info(script.hash, f"Starting {script.name} ({script.version})",
                                     name=script_name)
                    script.run()
                    self.logger.info(script.hash, f"Script '{script.name} ({script.version})' finished",
                                     name=script_name)
                except Exception as e:
                    self.logger.critical(script.hash, f"Script crash! str({e})", name=script_name)
            else:
                self.logger.critical(script.hash, f"Missing settings: {', '.join(settings)}",
                                     name=script_name)


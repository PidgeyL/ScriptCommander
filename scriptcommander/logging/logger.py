import click
import logging

from scriptcommander.database import DatabaseLayer
from scriptcommander.tools    import Singleton


class ScriptLogger(metaclass=Singleton):
    def __init__(self):
        self.dbl = DatabaseLayer()


    def _tty(self, feeder_hash, level, text, name=None):
        if name:
            click.echo(f"{name}:{level}:{text}")
        else:
            click.echo(f"{feeder_hash}:{level}:{text}")


    def debug(self, feeder_hash, text, name=None):
        self._tty(feeder_hash, 'DEBUG', text, name)
        self.dbl.add_log(feeder_hash, 'debug', text)


    def info(self, feeder_hash, text, name=None):
        self._tty(feeder_hash, 'INFO', text, name)
        self.dbl.add_log(feeder_hash, 'info', text)


    def warn(self, feeder_hash, text, name=None):
        self._tty(feeder_hash, 'WARN', text, name)
        self.dbl.add_log(feeder_hash, 'warning', text)


    def error(self, feeder_hash, text, name=None):
        self._tty(feeder_hash, 'ERROR', text, name)
        self.dbl.add_log(feeder_hash, 'error', text)


    def critical(self, feeder_hash, text, name=None):
        self._tty(feeder_hash, 'CRIT', text, name)
        self.dbl.add_log(feeder_hash, 'critical', text)

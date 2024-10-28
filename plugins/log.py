from datetime import datetime

from database import Database, DBModel
from plugin import BasePlugin


Database()


class LogEntry(DBModel):
    timestamp = datetime.now()
    text = ''

    def get_date(self):
        parsed = datetime.fromisoformat(str(self.timestamp))
        return parsed.strftime('%Y-%m-%d')

    def get_time(self):
        parsed = datetime.fromisoformat(str(self.timestamp))
        return parsed.strftime('%H:%M')

    def __repr__(self):
        return f'{self.get_time()}: {self.text}'

    def get_display(self, full=False):
        if full:
            return f'{self.get_date()}|{self.get_time()}: {self.text}'
        else:
            return repr(self)


class Plugin(BasePlugin):
    '''
    Add and display log entries
    '''
    def _add_log(self, text):
        entry = LogEntry(
            text=text,
            timestamp=datetime.now()
        )
        entry.save()
        return entry

    def _display_log(self, full):
        for i, entry in enumerate(LogEntry.find()):
            print(i, entry.get_display(full))

    def _clear_log(self):
        for entry in LogEntry.find():
            entry.delete()

    def run_command(self, args):
        if args == ['--full']:
            self._display_log(True)
        elif args == ['--reset']:
            self._clear_log()
        elif args:
            print(self._add_log(' '.join(args)))
        else:
            self._display_log(False)

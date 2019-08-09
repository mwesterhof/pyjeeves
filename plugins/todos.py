from database import Database, DBModel
from plugin import BasePlugin


Database()


class TodoEntry(DBModel):
    done = 0
    text = ''

    def __repr__(self):
        check = '[X]' if self.done else '[ ]'
        return f'{self.text} {check}'


class Plugin(BasePlugin):
    '''
    Add and manage TODO notes
    '''
    def _display_todos(self):
        print('Todo items:')
        for i, entry in enumerate(TodoEntry.find()):
            print(i, entry)

    def _get_todo_for_idx(self, idx):
        for i, entry in enumerate(TodoEntry.find()):
            if i == idx:
                return entry

    def _add_todo(self, text):
        entry = TodoEntry(text=text)
        entry.save()

    def _delete_todo(self, idx):
        self._get_todo_for_idx(idx).delete()

    def _toggle_todo(self, idx):
        entry = self._get_todo_for_idx(idx)
        entry.done = 1 - entry.done
        entry.save()

    def run_command(self, args):
        if args:
            if args[0] == 'add':
                text = ' '.join(args[1:])
                self._add_todo(text)
            elif args[0] == 'del':
                idx = int(args[1])
                self._delete_todo(idx)
            elif args[0] == 'toggle':
                idx = int(args[1])
                self._toggle_todo(idx)

        self._display_todos()

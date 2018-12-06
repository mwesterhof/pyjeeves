import webbrowser

from database import Database, DBModel
from plugin import BasePlugin


Database()


class TabConfig(DBModel):
    name = ''

    def __repr__(self):
        return self.name


class TabLink(DBModel):
    parent = TabConfig
    url = ''

    def save(self, *args, **kwargs):
        if not (self.url.startswith('http://') or
                self.url.startswith('https://')):
            self.url = 'http://' + self.url
        return super(TabLink, self).save(*args, **kwargs)

    def __repr__(self):
        return self.url


class Plugin(BasePlugin):
    '''
    Browser tabs management
    '''
    def _print_title(self, title, spacer=2):
        print('\n' * spacer)
        print(title)
        print('-' * len(title))

    def run_command(self, args):
        if args:
            config = TabConfig.find(name=args[0])[0]
            self.open_links(config)
        else:
            opt = self.show_root()
            if opt:
                self.show_group(opt)

    def show_root(self):
        self._print_title('Browser tab groups')
        configs = TabConfig.find()

        for i, group in enumerate(configs):
            links = TabLink.find(parent=group.pk)
            print('[{0}]: <{1}> ({2} links)'.format(
                i,
                group,
                len(links)
            ))

        try:
            opt = input('Enter a number (or a name to add a new group): ')
            opt = int(opt)
        except ValueError:
            tc = TabConfig(name=opt)
            tc.save()
            return tc
        return configs[opt]

    def show_group(self, config):
        self._print_title(config.name)
        links = TabLink.find(parent=config.pk)
        for i, link in enumerate(links):
            print('[{0}]: >> {1}'.format(i, link))
        opt = input('(a)dd, (e)dit, (r)emove, (o)pen: ').upper()
        if 'ADD'.startswith(opt):
            url = input('url: ')
            TabLink(url=url, parent=config.pk).save()
        elif 'EDIT'.startswith(opt):
            opt = int(input('index: '))
            url = input('url: ')
            link = links[opt]
            link.parent = config.pk
            link.url = url
            link.save()
        elif 'REMOVE'.startswith(opt):
            opt = int(input('index (-1 for all): '))
            if opt == -1:
                for tl in TabLink.find(parent=config.pk):
                    tl.delete()
            else:
                links[opt].delete()
            if not len(TabLink.find(parent=config.pk)):
                config.delete()
        elif 'OPEN'.startswith(opt):
            self.open_links(config)

    def open_links(self, config):
        links = TabLink.find(parent=config.pk)
        for i, link in enumerate(links):
            if i == 0:
                webbrowser.open_new(link.url)
            else:
                webbrowser.open_new_tab(link.url)

from plugin import BasePlugin, get_plugins


class Plugin(BasePlugin):
    '''
    Gathers the dependencies for all the plugins
    '''
    def run_command(self, args):
        gathered_deps = []
        for plugin_name in get_plugins():
            plugin = __import__(plugin_name[0])
            gathered_deps.extend(plugin.Plugin.dependencies)
        for dep in sorted(list(set(gathered_deps))):
            print dep

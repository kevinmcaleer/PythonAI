# Skill Loader
import importlib

class PluginInterface:
    """ A pluging has a single function called initialize"""

    @staticmethod
    def initialize() -> None:
        """ Initialize the plugin """
        
def import_module(name:str) -> PluginInterface:
    return importlib.import_module(name) # type: ignore

def load_skills(plugins: list[str])->None:
    """ Load the plugins """
    for plugin_name in plugins:
       plugin = import_module(plugin_name)
       plugin.initialize()

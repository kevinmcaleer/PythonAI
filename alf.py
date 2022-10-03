from ai import AI
from datetime import datetime
from skills import factory, loader
from plugins import plugin_loader, plugin_factory
import json
from eventhook import Event_hook
import sys

alf = AI()

# Setup events for plugins to attach to
alf.start = Event_hook()
alf.stop = Event_hook()

command = ""

# load the skills
with open("./skills/skills.json") as f:
    data = json.load(f)

    # load the plugins
    loader.load_skills(data["plugins"])

skills = [factory.create(item) for item in data["skills"]]
print(f'skills: {skills}')

# Load the plugins
with open("./plugins/plugins.json") as f:
    plugin_data = json.load(f)
    print(f'plugins: {plugin_data["plugins"]}')
    # load the plugins
    plugin_loader.load_plugins(plugin_data["plugins"])

plugins = [plugin_factory.create(item) for item in plugin_data["items"]]

# Register all the plugins
for item in plugins:
    item.register(alf)

alf.start.trigger()
alf.say("Hello")
command = ""
while True and command not in ["good bye", 'bye', 'quit', 'exit','goodbye', 'the exit']:
    command = ""
    command = alf.listen()
    if command:
        command = command.lower()
        print(f'command heard: {command}') 
        for skill in skills:
            if command in skill.commands(command):
                skill.handle_command(command, alf)

alf.say("Goodbye!")

# tell the plugins the server is shutting down
print('telling triggers to stop')
alf.stop.trigger()
print('telling ai to stop')
alf.stop_ai()
print('deleting ai')
del(alf)
print('done')


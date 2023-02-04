from ai import AI
from skills import factory, loader
from plugins import plugin_loader, plugin_factory
import json
from eventhook import Event_hook
import sys

akulai = AI()

# Setup events for plugins to attach to
akulai.start = Event_hook()
akulai.stop = Event_hook()

# Load the skills and plugins once and store the data in memory
with open("./skills/skills.json") as f:
    skills_data = json.load(f)
with open("./plugins/plugins.json") as f:
    plugins_data = json.load(f)

# Load the skills
loader.load_skills(skills_data["plugins"])
skills = [factory.create(item) for item in skills_data["skills"]]

# Load the plugins
plugin_loader.load_plugins(plugins_data["plugins"])
plugins = [plugin_factory.create(item) for item in plugins_data["items"]]

# Register all the plugins
for item in plugins:
    item.register(akulai)

akulai.start.trigger()
akulai.say("Hello")

while True:
    command = akulai.listen().lower()
    if command in ["good bye", 'bye', 'quit', 'exit','goodbye', 'the exit']:
        break
    print(f'command heard: {command}')
    for skill in skills:
        if command in skill.commands(command):
            skill.handle_command(command, akulai)
            break

akulai.say("Goodbye!")

# tell the plugins the server is shutting down
print('telling triggers to stop')
akulai.stop.trigger()
print('telling ai to stop')
akulai.stop_ai()
print('deleting ai')
del(akulai)
print('done')

from typing import Protocol
from skills.skill import Skill
from skills import factory, loader
import json
from dataclasses import dataclass

@dataclass
class Hello_skill():
    name = "hello_world"
    def commands(self, command:str):
        return ['hello', 'hi', 'hey']
    def handle_command(self, command:str):
        print("Hello")
        return "Hello"

@dataclass
class Good_bye_skill():
    name = "good_bye"
    def commands(self, command:str):
        return ['goodbye', 'bye', 'quit']
    def handle_command(self, command: str):
        print('goodbye')
        return "goodbye"

class SkillFactory(Protocol):
    """
    Factory that represents a skill
    The factory doesn't maintain any instance it creates

    """

    def get_skill(self)->Skill:
        """ Returns a new skill instance """

class Hello_world_factory():
    def get_skill(self)->Skill:
        return Hello_skill()

class Good_bye_factory():
    def get_skill(self) -> Skill:
        return Good_bye_skill()

# register the skills
factory.register('hello_world', Hello_skill)
factory.register('good_bye', Good_bye_skill)

with open("./skills/skills.json") as f:
    data = json.load(f)

    # load the plugins
    loader.load_skills(data["plugins"])
print(data["skills"])
skills = [factory.create(item) for item in data["skills"]]
print(f'skills: {skills}')
command = "bye"

for skill in skills:

    if command in skill.commands(command):
        skill.handle_command(command)


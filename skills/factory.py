from skills.skill import Skill
from typing import Callable, Any

skill_creation_funcs: dict[str, Callable[..., Skill]] = {}

def register(skill_name: str, creation_func: Callable[..., Skill]):
    """ Register a skill creation function """
    skill_creation_funcs[skill_name] = creation_func
    print(f'registered {skill_name}')

def unregister(skill_name: str):
    """ Unregister a skill creation function """
    skill_creation_funcs.pop(skill_name, None) 

def create(arguments:dict[str, Any])->Skill:
    """ Create a skill from a dictionary of arguments """
    args_copy = arguments.copy()
    skill_name = args_copy.pop('name')
    try:
        creation_func = skill_creation_funcs[skill_name]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown skill type: {skill_name}") from None
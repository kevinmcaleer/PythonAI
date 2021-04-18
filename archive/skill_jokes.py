# Jokes skill

from skills import Skill
import pyjokes

class Skill_Jokes(Skill):

    def __init__(self):
        print("installed Jokes Skill")

        self.name = "Jokes"
        self.version = 1.0
        self.actions = ['tell_me_a_joke']   

    def tell_me_a_joke(self):
        joke = pyjokes.get_joke()
        return joke
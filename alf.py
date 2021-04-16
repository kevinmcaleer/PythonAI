from ai import AI
from skill_weather import Skill_weather

alf = AI()

# alf.name = "Robbie the Robot"

weather = Skill_weather()
alf.register_skill(weather)
alf.list_skills()
while True:
    command = alf.listen()
    print("command was:",command)

    # do commands

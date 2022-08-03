from ai import AI
from time import sleep

alf = AI()
print ("say something")
message = ""
while True and message != 'good bye':
    message = alf.listen()
    if message:
        print(message)
    # sleep(0.5)
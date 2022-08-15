# PythonAI

An opensource AI Assistant for the Raspberry Pi
**By Kevin McAleer**

---

## 4 August Update

I'm returning to this project and will be doing a couple of new videos to improve the capabilities and to tidy up our code as its grown a bit unwieldly!

Here are a couple of things I'll be looking next:

- [x] a conversation history
- [X] a conversation API
- [X] a web interface (finally!)
- [X] a 'proper' skills framework, using plugin technology
- [X] an event framework to be able to add functionality via plugins

Google have stopped supporting the APi we previously used to convert speech audio to text, so I've not moved to an offline library called Vosk. Its very easy to setup - just type:

``` bash
pip install vosk
```

and you'll install the main library for Python.
You'll also need to download a model from <https://alphacephei.com/vosk/models>. I went with the `vosk-model-en-us-0.22` model, which although large is ery accurate. To install the model, just unzip the vosk-model-en-us-0.22.zip file and rename the unzipped folder to `model` and put that in the root of the git repository.

## Code Refactor

Since I started this project I've learned a lot more about Python, and Python itself has undergone many minor releases.
I've refactored almost all the code from the original project to make it easier to read, maintain and extend. Each skill now as a separate skill file that contains everything associated with that skill, and there is a new skill framework for importing the skills at runtime. This means we can add new skills without having to touch the main program.

The new skills framework mean that adding a new conversation history was very simple - I was even able to quickly add an API on top of the conversation history so we can read that in and dynamically update it using some javascript (and jQuery to pull in the convesation history data from the API).

## Skills framework

The new skills framework is very simple to implement:

1. Create a new python file in the `skills` folder
2. add a new class such as:

``` python
@dataclass
class Insults_skill:
    name = 'insults'
    
    def commands(self, command:str):
        return ['insult me', 'tell me an insult', 'give me an insult', 'roast me']
        
    def handle_command(self, command:str, ai:AI):
       ai.say('you are a worm')

def initialize():
    factory.register('insult_skill', Insult_skill)

```

3. Update the `skills.json` file to include the new skill:

``` json
{
    "plugins": ["skills.goodday", "skills.weather", "skills.facts", "skills.jokes", "skills.calendar", "skills.insult"],
    "skills": [
        {
            "name": "weather_skill"
        },
        {
            "name": "facts_skill"
        },
        {
            "name": "jokes_skill"
        },
        {
            "name": "goodday_skill"
        },
        {
            "name": "calendar_skill"
        },
        {
            "name": "insult_skill"
        }
    ]
}
```

4. Run the `alf.py` Python program
5. The skills factory will load the `skills.json` file and create a new list of skills, including this new Insults skill.
The `commands` function within the skill returns all the words or phrases that the AI will listen for and then handle those requests by running the `handle_command` function.

---

Create an API key (its free) at <home.openweathermap.org>

## On Raspberry Pi

Make sure you have pyaudio and espeak installed:

```bash
sudo apt-get install espeak
sudo apt-get install python-audio 
```

## Respeaker (Microphone array Hardware for Raspberry Pi)

Using the respeaker hat from Seeed studios:

```bash
git clone https://github.com/respeaker/seeed-voicecard
cd seeed-voicecard
sudo ./install.sh
sudo reboot
```

If this doesn't work and you get ASLA error messages, try:

*It may probably happen that the driver won't compile with the latest kernel when raspbian rolls out new patches to the kernel. If so, please try sudo ./install.sh --compat-kernel which uses an older kernel but ensures that the driver can work.*

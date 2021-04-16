# PythonAI
**By Kevin McAleer**

---

Create an API key (its free) at <home.openweathermap.org>


## On Raspberry Pi

make sure you have pyaudio and espeak installed:

```bash
sudo apt-get install espeak
sudo apt-get install python-audio 
```

using the respeaker hat from Seeed studios:

```bash
git clone https://github.com/respeaker/seeed-voicecard
cd seeed-voicecard
sudo ./install.sh
sudo reboot
```
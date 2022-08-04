from dataclasses import dataclass
from ai import AI
import plugins.plugin_factory
from flask import Flask, render_template
import logging 
from threading import Thread

@dataclass
class Webui_plugin:
    name = 'webui'
    
    app = None
    ai = None

    def __init__(self):
        self.app = Flask(__name__)

    def index(self):
        
        return render_template('index.html')

    def start_flask_thread(self):
        """ Start flask thread """
        print("starting flask thread")
        self.app.add_url_rule('/', 'index', self.index)
        self.app.run(debug=False, host='0.0.0.0', port=8080)
        self.app.logger.setLevel(logging.ERROR)

    def start(self):
        print("starting Webui server")
        self.flask = Thread(target=self.start_flask_thread,args=())
        self.flask.start()
        return self

    def stop(self):
        # shutdown the flask server
        print("stopping webui server")
        self.flask.join()

    def register(self, ai:AI):
        self.ai = ai
        print("registering webui plugin - at start")
        self.ai.start.register(self.start)  
        self.ai.stop.register(self.stop)
        return self

def initialize():
    # register with Factory or plugin?
    plugins.plugin_factory.register('webui_plugin', Webui_plugin)
    
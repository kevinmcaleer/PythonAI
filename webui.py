from flask import Flask, render_template

APP = Flask(__name__)

@APP.route("/")
def index():
    
    return render_template("index.html")

def main():
    """ main event loop """
    
    APP.secret_key = 'development-key'
    APP.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
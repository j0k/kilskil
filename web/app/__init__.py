#from flask import Flask
#app = Flask(__name__)
from eve import Eve
app = Eve(__name__)

def log_every_get(resource, request, payload):
    #def pre_get_callback(resource, request, lookup):
    print('A GET request on the "{}" endpoint has just been received!\n{}'.format(resource, request))

app.on_post_GET += log_every_get
print("my dears!")

@app.route("/")
def hello():
    return "Hello Eva!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

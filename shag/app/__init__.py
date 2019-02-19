import numpy as np
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    texts = ["Шагай петушара!","Вы уволены!", "Ты тоже супер!"]
    hXs   = list(range(7))

    text  = np.random.choice(texts)
    hX    = np.random.choice(hXs)

    return "<html><h{hX}>{text}</h{hX}></html>".format(hX = hX, text=text)

if __name__ == "__main__":
    app.run()

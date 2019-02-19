from flask import Flask, render_template
import re, requests, json

app = Flask(__name__)

host = "http://a.kilskil.com:80/"


@app.route("/hi/<user>")
def hi(user):
    return render_template("hi.html", user=user)


@app.route("/skiller-<user>")
def skiller(user):
    url = host + "userSkillProgress?where={{\"username\":\"{user}\"}}".format(user=user)
    try:
        req = requests.get(url, timeout=30)
        obj = json.loads(req.content.decode("utf-8"))
        item = obj["_items"][0]
        data = item

        for skill in data["skills"]:
            logo = skill["materials"]["logo"]

            if logo not in ["meditate", "art", "acro_fit", "music", "plant", "psymind"]:
                logo = "skill"

            skill["logo"] = logo

            num, count = skill["progress"]["num"], skill["count"]
            perc       = int(num*1.0 /count * 100)
            perc       = min(perc, 100)
            skill["perc"] = perc

        print(data)
        return render_template("userSkillProgress.html", data=data)
    except Exception as e:
        return render_template("hi.html", user=str(e))

@app.route('/<path:path>')
def static_file(path):
    print(path)
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="1234")

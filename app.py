from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev-secret"  # Required for sessions


# Home route
@app.route("/")
def home():
    return render_template("home.html")


# /sign
@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            entry = {
                "name": name,
                "time": datetime.now().strftime("%H:%M:%S")
            }
            guestbook = session.get("guestbook", [])
            guestbook.insert(0, entry)  # newest first
            session["guestbook"] = guestbook
        return redirect(url_for("guestbook"))

    return render_template("sign.html")


# /guestbook
@app.route("/guestbook")
def guestbook():
    entries = session.get("guestbook", [])
    return render_template("guestbook.html", entries=entries)


# /clear
@app.route("/clear")
def clear():
    session["guestbook"] = []
    return redirect(url_for("guestbook"))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
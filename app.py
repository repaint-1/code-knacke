from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DIGITS = "1234567890"
CODE_LENGTH = 4
SPECIAL_CODE = "Rolex"


def generate_code():
    return ''.join(random.choices(DIGITS, k=CODE_LENGTH))


@app.route("/", methods=["GET", "POST"])
def index():
    if "code" not in session:
        session["code"] = generate_code()
        session["attempts"] = 0
        session["show_code"] = False

    message = ""
    show_code = session.get("show_code", False)
    attempts = session.get("attempts", 0)

    if request.method == "POST":
        guess = request.form.get("guess")

        if guess == SPECIAL_CODE:
            return render_template("win.html", special=True)

        if len(guess) != CODE_LENGTH or not guess.isdigit():
            message = f"Bitte gib einen {CODE_LENGTH}-stelligen Zahlencode ein."
        else:
            session["attempts"] += 1
            code = session["code"]

            if guess == code:
                return render_template("win.html", special=False, attempts=session["attempts"])
            elif guess < code:
                message = "Der Code ist höher als deine Eingabe."
            else:
                message = "Der Code ist niedriger als deine Eingabe."

    return render_template("index.html", 
                           message=message,
                           attempts=attempts,
                           show_code=show_code,
                           current_code=session.get("code") if show_code else None)


@app.route("/reset")
def reset():
    session.pop("code", None)
    session.pop("attempts", None)
    session["show_code"] = False
    return redirect(url_for("index"))


@app.route("/reveal")
def reveal():
    session["show_code"] = True
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

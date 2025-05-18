from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'geheim'

def generate_code():
    return "".join(random.choices("0123456789", k=4))

@app.route("/", methods=["GET", "POST"])
def index():
    if 'code' not in session:
        session['code'] = generate_code()
        session['guesses'] = []
        session['mode'] = 'normal'

    message = ""
    hint = ""
    remaining = 10_000 - len(session['guesses'])  # 10.000 mögliche Kombinationen von 0000–9999

    if request.method == "POST":
        guess = request.form.get("guess", "")

        if guess == "Rolex":
            session['mode'] = 'rolex'
            message = "🔓 Rolex-Modus aktiviert! Du bekommst Hinweise."
        elif guess == "reset":
            session.clear()
            return redirect(url_for("index"))
        else:
            if session['mode'] == 'rolex':
                if guess in session['guesses']:
                    message = "❌ Diesen Code hast du schon probiert."
                else:
                    session['guesses'].append(guess)
                    remaining = 10000 - len(session['guesses'])

                    if guess == session['code']:
                        message = "🎉 Du hast den Code geknackt!"
                        session.clear()
                        return redirect(url_for("index"))
                    else:
                        if guess < session['code']:
                            hint = "🔼 Der richtige Code ist **größer**."
                        else:
                            hint = "🔽 Der richtige Code ist **kleiner**."
                        message = f"❌ Falscher Code. Noch {remaining} Kombinationen möglich."
            else:
                if guess == session['code']:
                    message = "🎉 Du hast den Code geknackt!"
                    session.clear()
                    return redirect(url_for("index"))
                else:
                    message = "❌ Falscher Code. Versuch es nochmal."

    return render_template("index.html", message=message, hint=hint,
                           mode=session.get('mode'), guesses=session.get('guesses', []), remaining=remaining)

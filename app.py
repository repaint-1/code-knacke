from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'geheim'

def generate_code():
    return ''.join(random.choices('1234567890', k=4))

@app.route("/", methods=["GET", "POST"])
def index():
    if "code" not in session:
        session["code"] = generate_code()
        session["attempts"] = 0
        session["show_code"] = False
        session["allow_hints"] = False

    feedback = ""
    code_reveal = ""

    if request.method == "POST":
        code_guess = request.form.get("code_guess")
        special_code = request.form.get("special_code")

        if special_code:
            if special_code.lower() == "rolex":
                session["allow_hints"] = True
                feedback = "✅ Spezialcode akzeptiert! Hinweise aktiviert."
            else:
                feedback = "❌ Falscher Spezialcode. Hinweise bleiben deaktiviert."

        elif code_guess:
            session["attempts"] += 1
            secret = session["code"]

            if code_guess == secret:
                return render_template("win.html", message=f"🎉 Du hast den Code in {session['attempts']} Versuchen geknackt!")

            if session["allow_hints"]:
                feedback_list = []
                for i in range(4):
                    if code_guess[i] == secret[i]:
                        feedback_list.append(f"Stelle {i+1}: ✔️ korrekt")
                    elif code_guess[i] > secret[i]:
                        feedback_list.append(f"Stelle {i+1}: 🔽 niedriger")
                    else:
                        feedback_list.append(f"Stelle {i+1}: 🔼 höher")
                feedback = "<br>".join(feedback_list)
            else:
                feedback = "❌ Falsche Kombination."

    if session.get("show_code"):
        code_reveal = f"(🔓 Geheimer Code: {session['code']})"

    return render_template("index.html", feedback=feedback, attempts=session["attempts"], code_reveal=code_reveal)

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect("/")

@app.route("/aufgeben", methods=["POST"])
def aufgeben():
    session["show_code"] = True
    return redirect("/")


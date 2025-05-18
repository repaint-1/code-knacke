from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'geheim'  # Für Sessions

def generate_code():
    return "".join(random.choices("0123456789", k=4))

@app.route("/", methods=["GET", "POST"])
def index():
    if 'code' not in session:
        session['code'] = generate_code()

    message = ""
    if request.method == "POST":
        guess = request.form.get("guess")
        if guess == session['code']:
            message = "🎉 Du hast es geschafft!"
            session['code'] = generate_code()  # Neuer Code fürs nächste Mal
        else:
            message = "❌ Falscher Code, versuch's nochmal."

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)

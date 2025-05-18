from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'  # <- Ersetze durch etwas Sicheres in Produktion

MAX_ATTEMPTS = 10000

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialisiere Spiel bei erster Anfrage
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['guesses'] = []

    message = None

    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
        except ValueError:
            message = "Bitte gib eine gültige Zahl ein."
            return render_template('index.html', message=message, guesses=session['guesses'], remaining=MAX_ATTEMPTS - len(session['guesses']))

        session['guesses'].append(guess)

        if guess < session['number']:
            message = "Zu niedrig!"
        elif guess > session['number']:
            message = "Zu hoch!"
        else:
            message = f"Richtig! Die Zahl war {session['number']}."
            number = session['number']
            guesses = session['guesses']
            session.clear()
            return render_template('win.html', number=number, guesses=guesses)

        if len(session['guesses']) >= MAX_ATTEMPTS:
            number = session['number']
            session.clear()
            return render_template('lose.html', number=number)

    remaining = MAX_ATTEMPTS - len(session['guesses'])
    return render_template('index.html', message=message, guesses=session['guesses'], remaining=remaining)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


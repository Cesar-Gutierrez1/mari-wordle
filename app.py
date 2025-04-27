from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

ANSWER = "MARI"


@app.route("/", methods=["GET", "POST"])
def home():
    if 'guesses' not in session:
        session['guesses'] = []

    message = ""

    if request.method == "POST":
        guess = request.form.get("guess", "").upper()

        if len(guess) != 4 or not guess.isalpha():
            message = "❌ Please enter a 4-letter word!"
        else:
            session['guesses'].append(guess)
            session.modified = True

            if guess == ANSWER:
                message = "🎉 Congratulations! You guessed it: MARI 🎉"
            else:
                feedback = ""
                for g_char, a_char in zip(guess, ANSWER):
                    if g_char == a_char:
                        feedback += "🟩"
                    elif g_char in ANSWER:
                        feedback += "🟨"
                    else:
                        feedback += "⬛"
                message = f"Feedback: {feedback}"

    # Create detailed guess info for coloring
    colored_guesses = []
    for guess in session['guesses']:
        letter_colors = []
        for i, g_char in enumerate(guess):
            if g_char == ANSWER[i]:
                letter_colors.append(('green', g_char))
            elif g_char in ANSWER:
                letter_colors.append(('yellow', g_char))
            else:
                letter_colors.append(('gray', g_char))
        colored_guesses.append(letter_colors)

    return render_template("index.html",
                           message=message,
                           colored_guesses=colored_guesses)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True, use_reloader=False)

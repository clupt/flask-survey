from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def show_survey():
    """ Returns a rendered template of the survey"""

    return render_template("survey_start.html", survey = survey)

@app.post("/begin")
def direct_user_to_question():
    """ Brings the user to questions"""
    #empty out list of responses
    session["responses"] = []
    return redirect("/questions/0")

@app.get("/questions/<int:question_num>")
def show_current_question(question_num):
    """ Takes in question number and shows html for form for that question"""

    # session["responses"] = responses
    question = survey.questions[question_num]
    responses = session["responses"]
    print("responses", responses)

    if responses is None:
        return redirect("/")

    if len(responses) == len(survey.questions):
        return redirect("/complete")

    if len(responses) != question_num:
        print("responses", responses)
        return redirect(f"/questions/{len(responses)}")


    return render_template("question.html",
        question_num = question_num,
        question = question)

@app.post("/answer")
def store_answer_redirect():
    """access and save response and redirect to next question"""

    choice = request.form['answer']

    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    if(len(responses) == len(survey.questions)):
        return redirect("/completion")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.get("/completion")
def completion():
    """sends questions and user reponses to completion page"""

    questions = survey.questions
    return render_template(
        "completion.html", questions=questions)

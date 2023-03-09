from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def show_survey():
    """ Returns a rendered template of the survey"""
    return render_template("survey_start.html", survey = survey)

@app.post("/begin")
def direct_user_to_question():
    """ Brings the user to questions"""
    return redirect("/questions/0")

@app.get("/questions/<int:question_num>")
def show_current_question(question_num):
    """ Takes in question number and shows html for form for that question"""
    question = survey.question[question_num]
    return render_template("question.html",
                           question_num = question_num,
                           question = question)

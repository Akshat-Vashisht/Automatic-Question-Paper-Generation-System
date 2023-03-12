from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
import random


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/instructions")
@login_required
def question_paper():
    return render_template("instructions.html", user=current_user)


@views.route("/generate", methods=["GET", "POST"])
@login_required
def generate_question_paper():
    file = request.files['excel_file']
    df = pd.read_excel(file)
    question = df["Question"]
    marks = df["Marks"]
    difficulty = df["Difficulty"]
    blooms = df["Blooms"]
    # Test hard code
    df = df[((df['Marks'] == 5) & (df['Difficulty'] == "Easy"))
            | ((df['Marks'] == 4) & (df['Difficulty'] == "Medium"))]
    df = df.sample(n=5, replace=False)
    return render_template("generate.html", user=current_user, df=df)

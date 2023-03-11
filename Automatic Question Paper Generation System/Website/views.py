from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/instructions")
@login_required
def question_paper():
    return render_template("instructions.html", user=current_user)

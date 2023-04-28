from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, request, render_template, send_file, session
import pandas as pd
from docx.shared import Inches
from io import BytesIO
from docx import Document
from docxtpl import DocxTemplate
from docx2pdf import convert
from fpdf import FPDF
import base64
import numpy as np

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/instructions")
@login_required
def question_paper():
    return render_template("instructions.html", user=current_user)


@views.route("/constraints", methods=["GET", "POST"])
@login_required
def basic_details():
    if request.method == "POST":
        max_marks = int(request.form.get("max_marks"))
        num_questions = int(request.form.get("num_questions"))
        session["max_marks"] = max_marks
        session["num_questions"] = num_questions
    return render_template("constraints.html", user=current_user, num_questions=num_questions)


@views.route("/generate", methods=["GET", "POST"])
@login_required
def generate_qp():
    if request.method == "POST":
        file = request.files.get("excel_file")
        question_marks = request.form.getlist("question_marks")
        question_difficulty = request.form.getlist("question_difficulty")
        df = pd.read_excel(file)
        finalDf = pd.DataFrame()
        max_marks = session.get("max_marks")
        num_questions = session.get("num_questions")
        for i in range(num_questions):
            mark = int(question_marks[i])
            diff = question_difficulty[i]
            temp = df[np.logical_and(
                df["Marks"] == mark, df["Difficulty"] == diff)]
            temp = temp.sample(n=1, replace=False)
            finalDf = pd.concat([finalDf, temp], ignore_index=True)

        print(finalDf)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="MIT ADT UNIVERSITY PAPER", align="C")
        pdf.ln()
        pdf.set_font("Arial", size=12)
        for i in range(0, num_questions):
            pdf.cell(10, 10, txt=f"Q{i+1}", ln=0)
            pdf.multi_cell(
                160, 10, txt=f" {finalDf['Question'][i]} ({finalDf['Marks'][i]})")

        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return render_template("generate.html", user=current_user, df=finalDf, document_pdf=pdf_base64)

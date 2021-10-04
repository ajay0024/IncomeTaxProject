from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import re

app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_number = db.Column(db.String(80), unique=True, nullable=False)
    section_title = db.Column(db.String(120), nullable=False)
    section_text = db.Column(db.Text, nullable=False)


db.create_all()


def treat_section_text(text, sec_num):
    final_text = text
    final_text = final_text.replace("\n", "<br/><br/>")
    regex = fr"^.*{sec_num}\.\s"
    final_text = re.sub(regex, "", final_text, 1)
    return final_text


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/income-tax-act/<page-num>")
def act_list():
    sections = Section.query.filter_by(section_number=section_num).first()
    return render_template("index.html")

@app.route("/section/<section_num>")
def section_view(section_num):
    section = Section.query.filter_by(section_number=section_num).first()
    text = treat_section_text(text=section.section_text, sec_num=section_num)

    return render_template("section_view.html", section=section, text=text)


if __name__ == "__main__":
    app.run(debug=True)

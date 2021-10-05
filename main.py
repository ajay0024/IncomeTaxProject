from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import markupsafe
import re

app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

ROWS_PER_PAGE=10

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_number = db.Column(db.String(80), unique=True, nullable=False)
    section_title = db.Column(db.String(120), nullable=False)
    section_text = db.Column(db.Text, nullable=False)


db.create_all()


@app.context_processor
def utility_processor():
    def treat_section_text(text, sec_num, **kwargs):
        final_text = text
        #TODO Rstrip to remove trailing br if length is fixed may have to use args/kwargs. rather than striping in HTML file
        final_text = final_text.replace("\n", "<br/><br/>")

        regex = fr"^.*{sec_num}\.\s"
        final_text = re.sub(regex, "", final_text, 1)
        if "chars" in kwargs:
            final_text=final_text[:kwargs['chars']]
        print(final_text)

        regex = r"<.{0,9}$"
        final_text = re.sub(regex, "", final_text)
        print(final_text)
        return final_text

    return dict(treat_section_text=treat_section_text)


# def treat_section_text(text, sec_num):
#     final_text = text
#     final_text = final_text.replace("\n", "<br/><br/>")
#     regex = fr"^.*{sec_num}\.\s"
#     final_text = re.sub(regex, "", final_text, 1)
#     return final_text


@app.route("/")
def home():
    return redirect(url_for("act_list", page=1))
    return render_template("index.html")


@app.route("/income-tax-act")
def act_list():
    page = request.args.get('page', 1, type=int)
    sections = Section.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template("index.html", sections=sections)


@app.route("/section/<section_num>")
def section_view(section_num):
    section = Section.query.filter_by(section_number=section_num).first()
    return render_template("section_view.html", section=section)


if __name__ == "__main__":
    app.run(debug=True)

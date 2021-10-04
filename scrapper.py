import sqlalchemy
from sqlalchemy import exc
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from crawler import Crawler
from data_handler import DataHandler


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

# Code for Scraping Sections from Income tax Website
START_LINK = "https://www.incometaxindia.gov.in/_layouts/15/dit/Pages/viewer.aspx?grp=Act&cname=CMSID&cval=102120000000077675&searchFilter=[{%22CrawledPropertyKey%22:1,%22Value%22:%22Act%22,%22SearchOperand%22:2},{%22CrawledPropertyKey%22:0,%22Value%22:%22Income-tax%20Act,%201961%22,%22SearchOperand%22:2},{%22CrawledPropertyKey%22:29,%22Value%22:%222021%22,%22SearchOperand%22:2}]&k=&IsDlg=0"
# START_LINK="https://www.incometaxindia.gov.in/_layouts/15/dit/Pages/viewer.aspx?grp=Act&cname=CMSID&cval=102120000000077635&searchFilter=[{%22CrawledPropertyKey%22:1,%22Value%22:%22Act%22,%22SearchOperand%22:2},{%22CrawledPropertyKey%22:0,%22Value%22:%22Income-tax%20Act,%201961%22,%22SearchOperand%22:2},{%22CrawledPropertyKey%22:29,%22Value%22:%222021%22,%22SearchOperand%22:2}]&k=&IsDlg=0"
command = ""

while command != "q":
    if command == "c":
        limit = int(input("Enter limit : "))
        crawler = Crawler(start_link=START_LINK)
        sections = crawler.start_crawling_onwards(limit=limit)
        for section in sections:
            print(section["section_text"])
            s = Section(section_title=section["section_title"], section_number=section["section_number"],
                        section_text=section["section_text"])
            try:
                db.session.add(s)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                print("Error during insertion command")

    command = input("Enter c to crawl and save, l to load data, q to quit : ")

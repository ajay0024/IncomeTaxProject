import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def make_section_url(num):
    url1 = "https://www.incometaxindia.gov.in/_layouts/15/dit/Pages/viewer.aspx?grp=Act&cname=CMSID&cval="
    url2 = '&searchFilter=[{"CrawledPropertyKey":1,"Value":"Act","SearchOperand":2},{"CrawledPropertyKey":0,"Value":"Income-tax Act, 1961","SearchOperand":2},{"CrawledPropertyKey":29,"Value":"2021","SearchOperand":2}]&k=&IsDlg=0'
    url = url1 + num + url2
    return url


class Section:
    def __init__(self, section_number, section_title, section_text):
        self.section_number = section_number
        self.section_code = 0
        self.section_text = section_text
        self.section_title = section_title

    def get_section_text(self):
        driver = webdriver.Firefox()
        driver.get(url=make_section_url(self.section_code))
        div = driver.find_element_by_class_name("viewerContent")
        print(div.text)
        driver.quit()
        return div.text

    def set_section_text(self, text):
        self.section_text = text

    def display(self):
        print(f"Section - {self.section_number}")
        print(f"Title - {self.section_title}")
        # print(self.section_text)

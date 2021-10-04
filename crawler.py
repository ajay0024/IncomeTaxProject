from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from section import Section
import time


class Crawler():
    def __init__(self, start_link):
        self.start_link = start_link
        self.driver = webdriver.Firefox()
        self.driver.get(url=start_link)
        self.sections = []

    def start_crawling_onwards(self, limit=9999):
        keep_crawling = True
        print(limit)
        count = 0
        while keep_crawling:
            time.sleep(3)
            section_number = self.driver.find_element_by_class_name("viewerActHeading").text
            # sec = Section()

            section_text_element = self.driver.find_element_by_class_name("viewerContent")
            section_text = section_text_element.text
            try:
                section_rows = section_text_element.find_elements_by_css_selector(".tx")
                bold_left_aligned_rows = []
                for row in section_rows:
                    if row.get_attribute("style") == "":
                        try:
                            left_bold_text = row.find_element_by_css_selector("b").text
                            bold_left_aligned_rows.append(left_bold_text)
                        except exceptions.NoSuchElementException:
                            pass
            #In case any stale element is found go back 1 page and come back 1 page
            except exceptions.StaleElementReferenceException:
                overlay = self.driver.find_element_by_id("overlaybx_page")
                WebDriverWait(self.driver, 100).until(EC.invisibility_of_element_located(overlay))
                button = WebDriverWait(self.driver, 100).until(
                    EC.element_to_be_clickable((By.ID, 'ViewerPreviousButton')))
                button.click()
                time.sleep(3)
                overlay = self.driver.find_element_by_id("overlaybx_page")
                WebDriverWait(self.driver, 100).until(EC.invisibility_of_element_located(overlay))
                button = WebDriverWait(self.driver, 100).until(
                    EC.element_to_be_clickable((By.ID, 'ViewerPreviousButton')))
                button.click()
                print("Met Stale Element Handing Exception")

            else:
            # TODO  How to Add Schedules
                try:
                    section_title = bold_left_aligned_rows[0]
                    section_number = bold_left_aligned_rows[1].strip('.')
                except IndexError:
                    section_title = ""
                    section_number = ""
                sec = {"section_number": section_number, "section_title": section_title, "section_text": section_text}
                self.sections.append(sec)
                count += 1
                print(count)
                if count >= limit:
                    keep_crawling = False

                overlay = self.driver.find_element_by_id("overlaybx_page")
                WebDriverWait(self.driver,100).until(EC.invisibility_of_element_located(overlay))
                button = WebDriverWait(self.driver, 100).until(
                    EC.element_to_be_clickable((By.ID, 'ViewerNextButton')))
                # self.driver.execute_script("arguments[0].style.visibility='hidden'", overlay)
                button.click()
        self.driver.quit()
        return self.sections

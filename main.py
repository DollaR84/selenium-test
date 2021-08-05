"""
Test email + selenium for test task.

Created on 04.08.2021

@author: Ruslan Dolovanyuk

"""

import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utils


COUNT_EMAIL = 15
COUNT_SYMBOLS = 10


class UkrNetMail:
    """Class for connect and process with ukr.net eMail."""

    def __init__(self):
        self.status = False
        self.__url__ = 'https://accounts.ukr.net/login'
        self.__driver = webdriver.Chrome(os.getenv('CHROME_DRIVER_PATH'))
        self.__driver.get(self.__url__)
        self.__wait = WebDriverWait(self.__driver, 10)
        if self.__wait.until(EC.title_contains("@ ukr.net")):
            self.status = True

    def login(self):
        """Send login and password to site for connect email."""
        field = self.__wait.until(EC.element_to_be_clickable((By.NAME, "login")))
        field.send_keys(os.getenv("UKRNET_LOGIN"))
        field = self.__wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        field.send_keys(os.getenv("UKRNET_PASSWORD"))
        field.send_keys(Keys.RETURN)

    def close(self):
        """Close webdriver with shutdown script."""
        self.__driver.quit()

    def create_email(self, to, subject, message):
        """Create and send email."""
        self.__wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='content']/button"))).click()
        field = self.__wait.until(EC.element_to_be_clickable((By.NAME, "to")))
        field.send_keys(to)
        field = self.__wait.until(EC.element_to_be_clickable((By.NAME, "subject")))
        field.send_keys(subject)
        field = self.__wait.until(EC.element_to_be_clickable((By.NAME, "editLinkBlock")))
        field.send_keys(message)
        field = self.__wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button primary send"))).click()

    def get_emails(self):
        """Get all email lists."""
        emails = {}
        for row in self.__wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr/td[@class='msglist__row-subject']"))):
            email_list = row.split('<strong> &nbsp;')
            emails[email_list[0]] = email_list[1]
        return emails

    def delete_emails(self):
        """Delete all email lists."""
        for checkbox in self.__wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr/td/input[@type='checkbox']"))):
            checkbox.click()
        self.__wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "controls-link remove"))).click()


def main():
    client = UkrNetMail()
    if client.status:
        client.login()
        email_to = ''.join([os.getenv("UKRNET_LOGIN"), '@ukr.net'])
        for _ in range(COUNT_EMAIL):
            client.create_email(email_to, utils.get_string(COUNT_SYMBOLS), utils.get_string(COUNT_SYMBOLS))
        emails = client.get_emails()
        client.del_emails()
        client.create_email(email_to, "Answer email", utils.create_email(emails))
        client.close()


if __name__ == '__main__':
    main()

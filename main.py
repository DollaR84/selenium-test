"""
Test email + selenium for test task.

Created on 04.08.2021

@author: Ruslan Dolovanyuk

"""

import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        time.sleep(1)
        if "@ ukr.net" in self.__driver.title:
            self.status = True

    def login(self):
        """Send login and password to site for connect email."""
        field = self.__driver.find_element_by_name("login")
        field.send_keys(os.getenv("UKRNET_LOGIN"))
        field = self.__driver.find_element_by_name("password")
        field.send_keys(os.getenv("UKRNET_PASSWORD"))
        field.send_keys(Keys.RETURN)

    def close(self):
        """Close webdriver with shutdown script."""
        self.__driver.quit()

    def create_email(self, to, subject, message):
        """Create and send email."""
        self.__driver.find_element_by_xpath("//div[@id='content']/button").click()
        time.sleep(1)
        field = self.__driver.find_element_by_name("to")
        field.send_keys(to)
        field = self.__driver.find_element_by_name("subject")
        field.send_keys(subject)
        field = self.__driver.find_element_by_name("editLinkBlock")
        field.send_keys(message)
        self.__driver.find_element_by_class_name("button primary send").click()

    def get_emails(self):
        """Get all email lists."""
        emails = {}
        for email in self.__driver.find_elements_by_xpath("//table/tbody/tr/td[@class='msglist__row-subject']"):
            email_list = email.split('<strong> &nbsp;')
            emails[email_list[0]] = email_list[1]
        return emails

    def delete_emails(self):
        """Delete all email lists."""
        emails = {}
        for checkbox in self.__driver.find_elements_by_xpath("//table/tbody/tr/td/input[@type='checkbox']"):
            checkbox.click()
        self.__driver.find_element_by_class_name("controls-link remove").click()


def main():
    client = UkrNetMail()
    if client.status:
        client.login()
        time.sleep(3)
        email_to = ''.join([os.getenv("UKRNET_LOGIN"), '@ukr.net'])
        for _ in range(COUNT_EMAIL):
            client.create_email(email_to, utils.get_string(COUNT_SYMBOLS), utils.get_string(COUNT_SYMBOLS))
            time.sleep(2)
        time.sleep(2)
        emails = client.get_emails()
        time.sleep(2)
        client.del_emails()
        time.sleep(2)
        client.create_email(email_to, "Answer email", utils.create_email(emails))
        time.sleep(2)
        client.close()


if __name__ == '__main__':
    main()

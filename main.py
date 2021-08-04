"""
Test email + selenium for test task.

Created on 04.08.2021

@author: Ruslan Dolovanyuk

"""

import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import gen


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

    def create_email(self):
        """Create email with random title and random body."""
        self.__driver.find_element_by_xpath("//div[@id='content']/button").click()
        


def main():
    client = UkrNetMail()
    if client.status:
        client.login()
        time.sleep(3)
        for _ in range(15):
            client.create_email()
            time.sleep(2)
        client.close()


if __name__ == '__main__':
    main()

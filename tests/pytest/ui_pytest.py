import os
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
DRIVER_PATH = '{}/Downloads/chromedriver'.format(os.environ['USER_PATH'])

class TestRestaurant(object):
    def setup_method(self):
        print('a')

    def test_search(self):
        print('test')

import os
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
DRIVER_PATH = '/Users/mizuki1998/Downloads/chromedriver'

class TestRestaurant(object):
    def setup_method(self):
        print('a')

    def test_search(self):
        print('test')

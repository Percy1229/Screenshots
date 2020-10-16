import time
import unittest
import os
import requests
from datetime import date

import schedule
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
DRIVER_PATH = '/Users/mizuki1998/Downloads/chromedriver'

# Select File for screenshots
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '/Users/mizuki1998/PycharmProjects/Screenshots/images/ticket.png')


# class PythonTest(unittest.TestCase):
#     def setUp(self):
    #     self.driver = webdriver.Chrome(executable_path=DRIVER_PATH,
    #                                    options=options)
    #     os.chdir('/Users/mizuki1998/PycharmProjects/Screenshots/images')
    #
    # def screenshot(self):
    #
    #     self.driver.get(
    #         'https://www.tokyodisneyresort.jp/ticket/sales_status/202011/'
    #     )
    #
    #     self.driver.execute_script("document.body.style.zoom='70%'")
    #
    #     """
    #         Selenium doesn't have function to remove code
    #         instead, use js(node)
    #     """
    #     self.driver.execute_script("""
    #                   var element = document.querySelector(".header-top");
    #                   if (element)
    #                       element.parentNode.removeChild(element);
    #                   """)
    #
    #     self.driver.execute_script("""
    #           var element = document.querySelector(".header-submenu");
    #           if (element)
    #               element.parentNode.removeChild(element);
    #           """)
    #
    #     self.driver.execute_script("""
    #           var element = document.querySelector(".header-globalmenu");
    #           if (element)
    #               element.parentNode.removeChild(element);
    #           """)
    #
    #     # scroll down
    #     target = self.driver.find_element_by_class_name('heading2')
    #     self.driver.execute_script('arguments[0].scrollIntoView();', target)
    #
    #     # get width and height of the page and set
    #     w = self.driver.execute_script('return document.body.scrollWidth;')
    #     h = self.driver.execute_script(
    #         'return document.body.scrollHeight;')
    #     self.driver.set_window_size(w, h)
    #
    #     # screenshot and save
    #     self.driver.save_screenshot(FILENAME)
    #     self.driver.quit()
    #
    #     # cut the screenshot
    #     screenshot = Image.open('ticket.png')
    #     width, height = screenshot.size
    #     left = width - 1010
    #     top = 0
    #     right = width - 400
    #     bottom = height - 62
    #     image = screenshot.crop((left, top, right, bottom))
    #     image.save('ticket.png')
    #
    #     url = 'https://notify-api.line.me/api/notify'
    #     # problem: token is exposed, hide it to bash.file
    #     line_notify_token = '0ZwJY98tP8TOoaD6Mj8Q7mh1jf5Duj2px4T91RCdtR4'
    #     headers = {'Authorization': 'Bearer ' + line_notify_token}
    #     payload = {'message': date.today()}
    #
    #     files = {'imageFile': open("ticket.png", "rb")}
    #     requests.post(url, data=payload, headers=headers, files=files)
    #     print("test")
    #
    # schedule.every(1).minutes.do(screenshot)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    #


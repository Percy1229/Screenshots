import os
import requests
import time
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

options = Options()

# set directory
image_dir = '../images/restaurant.png'

# chrome driver path
DRIVER_PATH = '{}/Downloads/chromedriver'.format(os.environ['USER_PATH'])

FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_dir)

restaurant_url = 'https://reserve.tokyodisneyresort.jp/sp/restaurant/search/'


class RestaurantPage:
    def __init__(self, day, title, pic_name, month=10):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH,
                                       options=options)
        self.day = day
        self.title = title
        self.pic_name = pic_name
        self.month = month
        os.chdir('{}/PycharmProjects/Screenshots/images'.format(
            os.environ['USER_PATH']))

    def search_restaurant(self, pick_restaurant=None):
        try:
            self.driver.get(restaurant_url)
        except NoSuchElementException:
            print('つながりにくい状況です')

        # open calendar
        calendar_img = self.driver.find_element_by_class_name(
            'ui-datepicker-trigger')
        calendar_img.click()
        time.sleep(1)

        # set month
        this_month = date.today().month
        if self.month > this_month:
            next_page = 'a.ui-datepicker-next.ui-corner-all'
            select_month = self.driver.find_element_by_css_selector(next_page)
            select_month.click()

        # set day
        day = self.driver.find_element_by_link_text(self.day)
        day.click()

        # num of pp
        select_pp = self.driver.find_element_by_id('searchAdultNum')
        select_num_pp = Select(select_pp)
        select_num_pp.select_by_value('2')

        # choose restaurant name
        if pick_restaurant is not None:
            restaurants = self.driver.find_element_by_id('restaurantNameCd')
            select_restaurant = Select(restaurants)
            get_options = select_restaurant.options
            for i in range(len(get_options)):
                restaurant_name = get_options[i].text
                if restaurant_name == pick_restaurant:
                    select_restaurant.select_by_visible_text(pick_restaurant)
                    break

        search_button = self.driver.find_element_by_id('searchButton')
        time.sleep(2)
        search_button.click()
        self.cur_url = self.driver.current_url

    def take_screenshot(self):
        try:
            self.driver.get(self.cur_url)
        except NoSuchElementException:
            print('つながりにくい状況です')

        # remove code
        self.driver.execute_script("""
                      var element = document.querySelector(".conditionBox");
                      if (element)
                          element.parentNode.removeChild(element);
                      """)

        # scroll down
        target = self.driver.find_element_by_class_name('listLink07')
        self.driver.execute_script('arguments[0].scrollIntoView();', target)

        # screenshot and save
        self.driver.save_screenshot(FILENAME)
        self.driver.quit()

    def send_line(self):
        notify_url = 'https://notify-api.line.me/api/notify'
        # problem: token is exposed, hide it to bash.file
        line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        files = {'imageFile': open("{}.png".format(self.pic_name), "rb")}
        text = '{title}\n指定された日付: {month}月{day}日'
        payload = {'message': text.format(title=self.title,
                                          month=self.month,
                                          day=self.day)}
        requests.post(notify_url, data=payload, headers=headers, files=files)


# お探しのレストランは現在、満席ですを出す(２つ)数を入力できるように
# 空いていた場合は、clickイベントを発火させ、スクショ、サイトのURLを送付

# restaurant = RestaurantPage('19', 'レストラン', 'restaurant', 11)
# restaurant.search_restaurant('ラ・タベルヌ・ド・ガストン')
# restaurant.take_screenshot()
# restaurant.send_line()

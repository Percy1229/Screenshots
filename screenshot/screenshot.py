import time
import os
import requests
import math
import re

# import schedule
from PIL import Image
from restaurant.restaurant import RestaurantPage
from selenium.common.exceptions import NoSuchElementException

# set image directory
image_dir = '../images/ticket.png'

# Select File for screenshots
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_dir)

ticket_url = "https://www.tokyodisneyresort.jp/ticket/sales_status/2020{}/"


class Ticket(RestaurantPage):
    def __init__(self, day):
        super(Ticket, self).__init__(day)

        self.title = 'チケット'
        self.pic_name = 'ticket-e'
        self.state = '枠が表示できません'
        self.circle = 0
        self.few = 0

        self.dl_state = 'TDL:現在、販売しておりません'
        self.l_date_state = ''
        self.l_total_date = ''
        self.dl_available_day = 0
        self.dl_circle_num = 0
        self.dl_few_num = 0

        self.ds_state = 'TDS:現在、販売しておりません'
        self.s_date_state = ''
        self.s_total_date = ''
        self.ds_available_day = 0
        self.ds_circle_num = 0
        self.ds_few_num = 0

        self.l_date = []
        self.dl_available_url = []
        self.s_date = []
        self.ds_available_url = []

    def get_info(self):
        self.driver.get(ticket_url.format(self.day))

        # total available day (TDR)
        # total x
        none = len(self.driver.find_elements_by_css_selector('div.is-none'))
        # total △
        self.few = len(self.driver.find_elements_by_css_selector('div.is-few'))
        # total -
        close = len(self.driver.find_elements_by_css_selector('div.is-close'))
        # total day of both park
        park = (len(self.driver.find_elements_by_css_selector('div.tdl')) - 6)
        total_day = park * 2
        without_circle = none + self.few + close
        # total ○
        self.circle = total_day - without_circle

        # total available days(DL)
        # total △
        dl_few = self.driver.find_elements_by_css_selector('div.tdl.is-few')
        self.dl_few_num = len(dl_few)
        # TDL modal info
        if self.dl_few_num > 0:
            for content in dl_few:
                # open modal
                content.find_element_by_tag_name('a').click()
                time.sleep(1)
                # get -月-日の販売状況
                l_date = self.driver.find_element_by_css_selector(
                    'h3.heading3')
                self.l_date.append(l_date.text)
                # day available △
                date_num = re.findall(r'\d+', l_date.text)
                self.l_total_date += '{} '.format(date_num[2])
                # get ticket available url
                btn = self.driver.find_element_by_css_selector('a.ticket-url')
                self.dl_available_url.append(btn.get_attribute('href'))
                # close modal
                mdl = self.driver.find_element_by_css_selector(
                    'div.modalContent')
                c_btn = mdl.find_element_by_css_selector('div.modalBtnClose')
                c_btn.click()
                time.sleep(1)

        # total x
        dl_none = self.driver.find_elements_by_css_selector('div.tdl.is-none')
        dl_none_num = len(dl_none)
        # open modal and check available day
        # now sold day
        sold_day = (self.few + none + self.circle) / 2
        # total ○
        few_none = self.dl_few_num + dl_none_num
        self.dl_circle_num = math.floor(sold_day - few_none)
        self.dl_available_day = self.dl_circle_num + self.dl_few_num

        # total available day (DS)
        # total △
        ds_few = self.driver.find_elements_by_css_selector('div.tds.is-few')
        self.ds_few_num = len(ds_few)

        # TDS modal info
        if self.ds_few_num > 0:
            for content in ds_few:
                # open modal
                content.find_element_by_tag_name('a').click()
                time.sleep(1)
                # get -月-日の販売状況
                s_date = self.driver.find_element_by_css_selector('h3.heading3')
                self.s_date.append(s_date.text)
                # day available △
                date_num = re.findall(r'\d+', s_date.text)
                self.s_total_date += '{} '.format(date_num[2])
                # get_url
                btn = self.driver.find_element_by_css_selector('a.ticket-url')
                self.ds_available_url.append(btn.get_attribute('href'))
                # close modal
                mdl = self.driver.find_element_by_css_selector(
                    'div.modalContent')
                c_btn = mdl.find_element_by_css_selector('div.modalBtnClose')
                c_btn.click()
                time.sleep(1)

        # total x
        ds_none = self.driver.find_elements_by_css_selector('div.tds.is-none')
        ds_none_num = len(ds_none)
        # total ○
        ds_few_none = self.ds_few_num + ds_none_num
        self.ds_circle_num = math.floor(sold_day - ds_few_none)
        self.ds_available_day = self.ds_circle_num + self.ds_few_num

    def take_pic(self):
        # problem: need to split code - add self to define cal or message
        self.driver.execute_script("document.body.style.zoom='70%'")

        """
            Selenium doesn't have function to remove code
            instead, use js(node)
        """
        self.driver.execute_script("""
                              var element = document.querySelector(
                              ".header-top");
                              if (element)
                                  element.parentNode.removeChild(element);
                              """)

        self.driver.execute_script("""
                      var element = document.querySelector(".header-submenu");
                      if (element)
                          element.parentNode.removeChild(element);
                      """)

        self.driver.execute_script("""
                      var element = document.querySelector(
                      ".header-globalmenu");
                      if (element)
                          element.parentNode.removeChild(element);
                      """)

        # scroll down
        target = self.driver.find_element_by_class_name('heading2')
        self.driver.execute_script('arguments[0].scrollIntoView();', target)

        # get width and height of the page and set
        w = self.driver.execute_script('return document.body.scrollWidth;')
        h = self.driver.execute_script(
            'return document.body.scrollHeight;')
        self.driver.set_window_size(w, h)

        # screenshot and save
        self.driver.save_screenshot(FILENAME)

    # problem: too long func so need to split search-available
    def search_dl_available(self):
        try:
            i = 0
            for url in self.dl_available_url:
                self.driver.get(url)
                time.sleep(5)
                caution = self.driver.find_elements_by_css_selector(
                    'p.text-caution')
                if len(caution) == 3:
                    # pass
                    i += 1
                    time.sleep(2)
                else:
                    print(self.l_date[i])
                    i += 1
                    cards = self.driver.find_elements_by_css_selector(
                        'div.search-ticket-card')
                    # num of cards
                    for card in cards:
                        # passport type
                        passport = card.find_element_by_css_selector(
                            'h4.heading-cont-top')
                        print(passport.text)
                        card.click()
                        time.sleep(3)
                        # 東京ディズニーランド
                        tdl_name = self.driver.find_element_by_class_name(
                            'search-1day-01')
                        print(tdl_name.text)
                        # 9:00 ~ 21:00 or 販売しておりません
                        sell_tdl = self.driver.find_element_by_class_name(
                            'search-1day-time-01')
                        print(sell_tdl.text)
                        print('#' * 10)
                        time.sleep(2)
                        back = self.driver.find_element_by_css_selector(
                            'a.search-slide-back')
                        back.click()
                        time.sleep(2)

        except NoSuchElementException:
            print('ただいまつながりにくい状況です')

    def search_ds_available(self):
        try:
            i = 0
            times = 0
            for url in self.ds_available_url:
                times += 1
                self.driver.get(url)
                time.sleep(2)
                caution = self.driver.find_elements_by_css_selector(
                    'p.text-caution')
                if len(caution) == 3:
                    # pass
                    i += 1
                    time.sleep(2)
                else:
                    print(self.s_date[i])
                    i += 1
                    cards = self.driver.find_elements_by_css_selector(
                        'div.search-ticket-card')
                    for card in cards:
                        # passport type
                        title = card.find_element_by_css_selector(
                            'h4.heading-cont-top')
                        print(title.text)
                        card.click()
                        time.sleep(3)
                        # 東京ディズニーシー
                        tds_name = self.driver.find_element_by_class_name(
                            'search-1day-02')
                        print(tds_name.text)
                        # 9:00 ~ 21:00 or 販売しておりません
                        sell_tds = self.driver.find_element_by_class_name(
                            'search-1day-time-02')
                        print(sell_tds.text)
                        time.sleep(1)
                        back = self.driver.find_element_by_css_selector(
                            'a.search-slide-back')
                        back.click()
                        time.sleep(2)
                time.sleep(2)
                if len(self.ds_available_url) == times:
                    self.driver.quit()

        except NoSuchElementException:
            print('つながりにくい状況です')

    def set_message(self):
        # set a message for line(TDR)
        if self.circle > 0:
            self.state = 'TDR:残り{}枠です'.format(self.circle + self.few)
        elif self.circle == 0 and self.few > 0:
            self.state = 'TDR:残り{}枠のみです'.format(self.few)
        elif self.circle == self.few:
            self.state = '現在、枠はありません'

        # set a message for line(TDL)
        if self.dl_available_day > 0:
            self.dl_state = 'TDL: ○ {} + △ {} = 残り{}枠です'.format(
                self.dl_circle_num, self.dl_few_num, self.dl_available_day)

        if self.l_total_date:
            self.l_date_state = '日付: {}'.format(self.l_total_date)

        # set a message for line(TDS)R
        if self.ds_available_day > 0:
            self.ds_state = 'TDS: ○ {} + △ {} = 残り{}枠です'.format(
                self.ds_circle_num, self.ds_few_num, self.ds_available_day)

        if self.s_total_date:
            self.s_date_state = '日付: {}'.format(self.s_total_date)

    def set_picture(self):
        # resize and cut the screenshot
        screenshot = Image.open('ticket.png')
        width, height = screenshot.size
        left = width - 1010
        top = 0
        right = width - 400
        bottom = height - 50
        image = screenshot.crop((left, top, right, bottom))
        image.save('{}.png'.format(self.pic_name))

    def send_line(self):
        notify_url = 'https://notify-api.line.me/api/notify'
        border = '-' * 5
        # problem: token is exposed, hide it to bash.file
        line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        text = '{title}\n{day}月\n{state}\n{b}\n{dl}\n{lds}\n{b}\n{ds}\n{sds}'
        text = text.format(title=self.title,
                           day=self.day,
                           state=self.state,
                           b=border,
                           dl=self.dl_state,
                           lds=self.l_date_state,
                           ds=self.ds_state,
                           sds=self.s_date_state)
        payload = {'message': text}
        files = {'imageFile': open("{}.png".format(self.pic_name), "rb")}
        requests.post(notify_url, data=payload, headers=headers, files=files)


# activate definition at a specified time
# a = Screenshot()
# schedule.every().day.at("13:27").do(a.take_screenshot)
# while True:
#     schedule.run_pending()
#     time.sleep(2)

# ticket for this month
# ticket1 = Ticket('10')
# ticket1.get_info()
# ticket1.take_pic()
# ticket1.set_message()
# ticket1.set_picture()
# ticket1.send_line()
#
# time.sleep(1)


# ticket for next month
ticket2 = Ticket('11')
ticket2.get_info()
ticket2.take_pic()
ticket2.search_dl_available()
ticket2.search_ds_available()
ticket2.set_message()
ticket2.set_picture()
ticket2.send_line()

# time.sleep(1)
#
# # # Restaurant for this month only
# restaurant = RestaurantPage('19', 11, 'ラ・タベルヌ・ド・ガストン')
# restaurant.search_restaurant()
# restaurant.take_pic()
# restaurant.send_line()

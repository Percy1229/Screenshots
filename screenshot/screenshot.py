import time
import os
import requests
import math
import re

# import schedule
from PIL import Image
from restaurant.restaurant import RestaurantPage

# set image directory
image_dir = '../images/ticket.png'

# Select File for screenshots
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_dir)

'https://www.tokyodisneyresort.jp/ticket/sales_status/202019/'

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
        self.dl_available_day = 0
        self.dl_circle_num = 0
        self.dl_few_num = 0

        self.ds_state = 'TDS:現在、販売しておりません'
        self.ds_available_day = 0
        self.ds_circle_num = 0
        self.ds_few_num = 0

        self.s_total_date = ''
        self.date_state = '{}が販売しています'

    def take_pic(self):
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
                content.find_element_by_tag_name('a').click()
                time.sleep(1)
                mdl = self.driver.find_element_by_css_selector(
                    'div.modalContent')
                c_btn = mdl.find_element_by_css_selector('div.modalBtnClose')
                c_btn.click()
                time.sleep(2)

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
        print(self.ds_few_num)

        # TDS modal info
        if self.ds_few_num > 0:
            for content in ds_few:
                # open modal
                content.find_element_by_tag_name('a').click()
                time.sleep(1)
                # get date
                s_date = self.driver.find_element_by_css_selector('h3.heading3')
                date_num = re.findall(r'\d+', s_date.text)
                self.s_total_date += '|{} '.format(date_num[2])
                print(self.s_total_date)
                # close modal
                div_modal = 'div.modalContent'
                mdl = self.driver.find_element_by_css_selector(div_modal)
                c_btn = mdl.find_element_by_css_selector('div.modalBtnClose')
                c_btn.click()
                time.sleep(2)

        # total x
        ds_none = self.driver.find_elements_by_css_selector('div.tds.is-none')
        ds_none_num = len(ds_none)
        # total ○
        ds_few_none = self.ds_few_num + ds_none_num
        self.ds_circle_num = math.floor(sold_day - ds_few_none)
        self.ds_available_day = self.ds_circle_num + self.ds_few_num

        # problem: need to split code - add self to define cal or message
        self.driver.execute_script("document.body.style.zoom='70%'")

        """
            Selenium doesn't have function to remove code
            instead, use js(node)
        """
        self.driver.execute_script("""
                      var element = document.querySelector(".header-top");
                      if (element)
                          element.parentNode.removeChild(element);
                      """)

        self.driver.execute_script("""
              var element = document.querySelector(".header-submenu");
              if (element)
                  element.parentNode.removeChild(element);
              """)

        self.driver.execute_script("""
              var element = document.querySelector(".header-globalmenu");
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
        self.driver.quit()

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

        # set a message for line(TDS)
        if self.ds_available_day > 0:
            self.ds_state = 'TDS: ○ {} + △ {} = 残り{}枠です'.format(
                self.ds_circle_num, self.ds_few_num, self.ds_available_day)

        if self.s_total_date:
            self.date_state = self.date_state.format(self.s_total_date)
            print(self.date_state)

    def set_picture(self):
        # resize and cut the screenshot
        screenshot = Image.open('ticket.png')
        width, height = screenshot.size
        left = width - 1010
        top = 0
        right = width - 400
        bottom = height - 62
        image = screenshot.crop((left, top, right, bottom))
        image.save('{}.png'.format(self.pic_name))

    def send_line(self):
        notify_url = 'https://notify-api.line.me/api/notify'
        # problem: token is exposed, hide it to bash.file
        line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        text = '{title}\n{day}月\n{state}\n{date_state}\n{dl_state}\n{ds_state}'
        text = text.format(title=self.title,
                           day=self.day,
                           state=self.state,
                           date_state=self.date_state,
                           dl_state=self.dl_state,
                           ds_state=self.ds_state)
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
ticket1 = Ticket('10')
ticket1.take_pic()
ticket1.set_message()
ticket1.set_picture()
ticket1.send_line()

time.sleep(1)


# ticket for next month
ticket2 = Ticket('11')
ticket2.take_pic()
ticket2.set_message()
ticket2.set_picture()
ticket2.send_line()

time.sleep(1)
#
# # Restaurant for this month only
restaurant = RestaurantPage('19', 11, 'ラ・タベルヌ・ド・ガストン')
restaurant.search_restaurant()
restaurant.take_pic()
restaurant.send_line()

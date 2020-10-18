import time
import os
import requests
import math

# import schedule
from PIL import Image
from restaurant.restaurant import RestaurantPage

# set image directory
image_dir = '../images/ticket.png'

# Select File for screenshots
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_dir)


ticket_url = "https://www.tokyodisneyresort.jp/ticket/sales_status/2020{}/"


class Ticket(RestaurantPage):
    def __init__(self, day, title, pic_name):
        super(Ticket, self).__init__(day, title, pic_name)

    def take_ticket_pic(self):
        self.driver.get(ticket_url.format(self.day))

        # total available day (TDR)
        # total x
        none = len(self.driver.find_elements_by_css_selector('div.is-none'))
        # total △
        few = len(self.driver.find_elements_by_css_selector('div.is-few'))
        # total -
        close = len(self.driver.find_elements_by_css_selector('div.is-close'))
        # total day of both park
        park = (len(self.driver.find_elements_by_css_selector('div.tdl')) - 6)
        total_day = park * 2
        # total x △ -
        without_circle = none + few + close
        # total ○
        circle = total_day - without_circle
        # set a message for line
        if circle > 0:
            self.state = 'TDR:残り{}枠です'.format(circle + few)
        elif circle == 0 and few > 0:
            self.state = 'TDR:残り{}枠のみです'.format(few)
        elif circle == few:
            self.state = '現在、枠はありません'

        # total available days(DL)
        # total △
        dl_few = self.driver.find_elements_by_css_selector('div.tdl.is-few')
        dl_few_num = len(dl_few)
        # total x
        dl_none = self.driver.find_elements_by_css_selector('div.tdl.is-none')
        dl_none_num = len(dl_none)
        # now sold day
        sold_day = (few + none + circle) / 2
        # total ○
        dl_circle_num = math.floor(sold_day - (dl_few_num + dl_none_num))
        dl_available_day = dl_circle_num + dl_few_num

        # set a message for line(DL)
        if dl_available_day > 0:
            self.dl_state = 'TDL: ○ {} + △ {} = 残り{}枠です'.format(
                dl_circle_num, dl_few_num, dl_available_day)
        else:
            self.dl_state = 'TDL:現在、販売しておりません'

        # total available day (DS)
        # total △
        ds_few = self.driver.find_elements_by_css_selector('div.tds.is-few')
        ds_few_num = len(ds_few)
        # total x
        ds_none = self.driver.find_elements_by_css_selector('div.tds.is-none')
        ds_none_num = len(ds_none)
        # total ○
        ds_circle_num = math.floor(sold_day - (ds_few_num + ds_none_num))
        ds_available_day = ds_circle_num + ds_few_num

        # set a message for line(DS)
        if ds_available_day > 0:
            self.ds_state = 'TDS: ○ {} + △ {} = 残り{}枠です'.format(
                ds_circle_num, ds_few_num, ds_available_day)

        else:
            self.ds_state = 'TDS:現在、販売しておりません'

        # TDL circle and few AM8:00

        # TDS circle and few AM8:00

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

    @staticmethod
    def cut_screenshot():
        # resize and cut the screenshot
        screenshot = Image.open('ticket.png')
        width, height = screenshot.size
        left = width - 1010
        top = 0
        right = width - 400
        bottom = height - 62
        image = screenshot.crop((left, top, right, bottom))
        image.save('ticket-e.png')

    def send_line(self):
        notify_url = 'https://notify-api.line.me/api/notify'
        # problem: token is exposed, hide it to bash.file
        line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        text = '{title}|{day}月\n{state}\n{dl_state}\n{ds_state}'
        text = text.format(title=self.title,
                           day=self.day,
                           state=self.state,
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
a = Ticket('12', 'チケット', 'ticket-e')
a.take_ticket_pic()
a.cut_screenshot()
a.send_line()

# print(os.environ)
time.sleep(1)


# ticket for next month
b = Ticket('11', 'チケット', 'ticket-e')
b.take_ticket_pic()
b.cut_screenshot()
b.send_line()

time.sleep(1)

# Restaurant for this month only
restaurant = RestaurantPage('19', 'レストラン', 'restaurant')
restaurant.search_restaurant(10)
restaurant.take_screenshot()
restaurant.send_line()

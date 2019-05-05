import configparser
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ExportBot:
    def __init__(self):
        config = configparser.RawConfigParser()
        config.read('./config.cfg')
        log_file = config['Export_params']['log_file']
        logging.basicConfig (format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
                             level=logging.INFO, filename=u'%s' % log_file)
        self.login = config['Export_params']['my_login']
        self.secret = config['Export_params']['my_secret']
        self.delay_between_likes = int (config['Export_params']['delay_between_likes'])
        self.quantity_likes =  int (config['Export_params']['quantity_likes'])


    def GetLogin (self):
        options = Options ( )
        options.add_argument ('--headless')
        options.add_argument ('--no-sandbox')
        # options.add_argument('--disable-gpu')  # applicable to windows os only
        self.driver = webdriver.Chrome (options=options, executable_path=r'/usr/bin/chromedriver')
        self.driver.get ('https://badoo.com/signin/?f=top')
        username = self.driver.find_element_by_class_name ('js-signin-login')
        username.send_keys (self.login)

        password = self.driver.find_element_by_class_name ('js-signin-password')
        password.send_keys (self.secret)

        form = self.driver.find_element_by_class_name ('sign-form__submit')
        form.submit ( )

        time.sleep (self.delay_between_likes)
        logging.info (u'Login user: %s success!' % (self.login))

    def GetLikes (self):
        try:
            self.driver.get ('https://badoo.com/encounters')

            with open ('index1.html', 'w') as w:
                w.write (self.driver.page_source)
                w.flush ( )

            for i in range (self.quantity_likes):
                time.sleep (self.delay_between_likes)
                self.driver.find_element_by_class_name ('js-profile-header-vote-yes').click ( )
                #html_name = 'index' + str (i) + '.html'
                logging.info (u'Like user %s is success!' % (i))
                # with open (html_name, 'w') as w:
                #     w.write (self.driver.page_source)
                #     w.flush ( )

        except :
            logging.info (u'selenium.common.exceptions.ElementClickInterceptedException')


our_bot = ExportBot()
our_bot.GetLogin()
our_bot.GetLikes()




import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime,timedelta
time_to_sleep = 10







class Intercity(webdriver.Chrome):
    def __init__(self, driverPath=r"C:\SeleniumDrivers", teardown=False):
        x = int(input('podaj trasę:  \n1:wro-krk \n2: krk-wro \n3:wro-kostrz \n4:kostrz-wro \n5:krk-kostrz \n6:kostrz-krk \n7:niest'))
        if x ==1:
            self.start_city = 'Wrocław'
            self.end_city = 'Kraków'
        elif x==2:
            self.start_city = 'Kraków'
            self.end_city = 'Wrocław'
        elif x ==3:
            self.start_city='Wrocław'
            self.end_city = "Kostrzyn" #todo add proper kostrzyn name
        elif x ==4:
            self.start_city="Kostrzyn"
            self.end_city =  'Wrocław'
        elif x==5:
            self.start_city = 'Kraków'
            self.end_city = 'Kostrzyn'
        elif x==6:
            self.start_city = 'Kostrzyn'
            self.end_city = 'Kraków'
        #     non standard route
        else:
            self.start_city = 'Kraków'
            self.end_city = 'Wrocław'

        y = int(input('dzisiaj 1: jutro 2:'))
        if y==1:
            self.date = datetime.today().strftime('%Y-%m-%d')
        else:
            self.date = (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')

        self.time = input('podaj godzine: np 12:30\n')


        self.driverPath = driverPath
        self.teardown = teardown
        os.environ['PATH'] = self.driverPath
        super().__init__()
        self.implicitly_wait(2 * time_to_sleep)
        self.maximize_window()

    def land_first_page(self):
        self.get('https://www.intercity.pl/pl/')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def fill_start_city(self):
        city_form = self.find_element(By.ID, "stname-0")
        city_form.send_keys(self.start_city)
        city_dropout = self.find_element(By.CSS_SELECTOR, f'a[title*="{self.start_city} "]')
        # default station in IC is main so nothing else o do here
        city_dropout.click()

    def fill_end_city(self):
        city_form = self.find_element(By.ID, "stname-1")
        city_form.send_keys(self.end_city)
        city_dropout = self.find_element(By.CSS_SELECTOR, f'a[title*="{self.end_city}"]')
        city_dropout.click()

    # todo: change default date
    def fill_date(self):
        date_form = self.find_element(By.ID, "date_picker")
        date_form.clear()
        date_form.send_keys(self.date)

    def fill_time(self,):
        time_form = self.find_element(By.ID, "ic-seek-time")
        time_form.clear()
        for i in range(5):
            time_form.send_keys(Keys.BACK_SPACE)
        time_form.send_keys(self.time)
        time_form.send_keys(Keys.ENTER)
        #  works with seek

    def seek(self):
        btn = self.find_element(By.CSS_SELECTOR, 'button[onclick="return grecaptcha.execute();"]')
        btn.click()
        self.implicitly_wait(5 * time_to_sleep)

    def fill_normal_people(self, n=0):
        people_elem = Select(self.find_element(By.ID, "liczba_n"))
        people_elem.select_by_value(f'{n}')
        self.implicitly_wait(time_to_sleep)

    def fill_students(self, n_students=1):
        students_elem = Select(self.find_element(By.ID, "liczba_u"))
        students_elem.select_by_value(f'{n_students}')
        self.implicitly_wait(time_to_sleep)

    # no easy way to automate further program waits until user clicks because of hidden btn

    def fill_discount_type(self):
        discount_elem = Select(self.find_element(By.ID, "kod_znizki"))
        discount_elem.select_by_value('99')
        self.implicitly_wait(time_to_sleep)
        # value 99

    # place for future methods for specifying compartments and type of cart

    def click_dalej_button(self):
        dalej_button = self.find_element(By.CSS_SELECTOR, 'input[data-modal-id="popup"]')
        dalej_button.click()
        self.implicitly_wait(time_to_sleep * 2)

    def fill_name_of_traveller(self, name='Adam Kowalski'):
        self.implicitly_wait(time_to_sleep)
        name_frame = self.find_element(By.ID, "imie_nazwisko_podroznego")
        name_frame.send_keys(name)
        self.implicitly_wait(time_to_sleep)

    def wrapper_find_train(self):
        self.land_first_page()
        self.fill_start_city()
        self.fill_end_city()
        self.fill_date()
        self.fill_time()
        self.seek()

    #         should work perfectly

    def wrapper_people_discount(self, n_normal_people=0, n_students=1):
        try:
            self.fill_normal_people(n_normal_people)
        except:
            print('some problem in finding a train, bad request or fill_normal_people')
            exit(-1)
        self.fill_students(n_students)
        self.fill_discount_type()
        self.click_dalej_button()

    def click_buy_no_register(self):
        no_register_elem = self.find_element(By.CSS_SELECTOR, 'a[href="/konto_gosc_rejestracja.jsp?"]')
        no_register_elem.click()
        self.implicitly_wait(time_to_sleep)

    def wrapper_user_data(self, name='Michał', last_name='Luchowski', email='michal.luchowski@vp.pl'):
        form_elem = self.find_element(By.CLASS_NAME, "quest_register_form ")
        # fieldset_names_lst = ['imie','nazwisko','email','powt_email']

        name_elem = form_elem.find_element(By.CSS_SELECTOR, 'input[name="imie"]')
        name_elem.send_keys(name)

        last_name_elem = form_elem.find_element(By.CSS_SELECTOR, 'input[name="nazwisko"]')
        last_name_elem.send_keys(last_name)

        email_elem = form_elem.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_elem.send_keys(email)

        repeat_email_elem = form_elem.find_element(By.CSS_SELECTOR, 'input[name="powt_email"]')
        repeat_email_elem.send_keys(email)
        self.implicitly_wait(time_to_sleep)

    def click_regulations_accept(self):
        checkbox = self.find_element(By.ID, "akceptacja")
        checkbox.click()
        self.implicitly_wait(time_to_sleep)

    def submit_user_data(self):
        user_data_frame_elem = self.find_element(By.ID, "icWebUserRegister")
        # todo possible integration with wrapper user data form_elem

        dalej_btn = user_data_frame_elem.find_element(By.CSS_SELECTOR, 'input[type="button"]')
        dalej_btn.click()
        self.implicitly_wait(time_to_sleep * 2)

    def click_zatwierdz_btn(self):
        submit_btn = self.find_element(By.CSS_SELECTOR, 'input[onclick="document.daneKlienta.submit()"]')
        submit_btn.click()
        self.implicitly_wait(time_to_sleep * 2)

    def send_thanks(self):
        print('thank u for using Intercity automation bot')

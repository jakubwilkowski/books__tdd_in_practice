import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do-app. She goes
        # to check out it's homepage

        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists.

        self.assertIn('Listy rzeczy do zrobienia', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('listę', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        # She types "buy peacock feathers" into a text box (Edith's hobby
        # is typing fly-fishing lures
        inputbox.send_keys('Kupić pawie pióra')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')

        # Teraz nowy użytkownik Frankek zaczyna korzystać z witryny

        ## Używamy nowej wersji przeglądarki internetowej, aby mieć pewność, że żadne
        ## informacje dotyczące Edyty nie zostana ujawnione na przyykład prze cookies

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franek odwiedza stronę główną
        # nie znajduje żadnych śladów listy Edyty
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertNotIn('zrobienia przynęty', page_text)

        # Franek tworzy nowa listę wprowadzając nowy element
        # Jego lista jest mniej interesujęca niż Edyty...
        inputbox =  self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Franek otrzymuje unikatowy adres URL prowadzący do listy
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Ponownie nie ma zadnego śladu po liscie Edyty
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertIn('Kupić mleko', page_text)

        # Usatysfakcjonowani oboje kłada się spać

    def test_layout_and_styling(self):
        # Edyta przeszła na stronę główną
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Zauważyła, ze pole tekstowe zostało elegancko wyśrodkowane
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=5
        )

        # Edyta utworzyła nową listę i zobaczyła,
        # że pole tekstowe nadal jest wyśrodkowane
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=5
        )

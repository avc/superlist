from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))

        # She starts typing some text for the new item and the error disappears.
        inputbox = self.item_input_box()
        inputbox.send_keys('Trying again')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        
        # And she can submit it successfully.
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Trying again')

        # Perversely, she now decides to submit a second blank list item
        self.item_input_box().send_keys(Keys.ENTER)
        
        # Again, the browser will not comply.
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))
        
        # And she can correct it by filling some text in
        inputbox = self.item_input_box()
        inputbox.send_keys('How about now?')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Trying again')
        self.wait_for_row_in_list_table('2: How about now?')
    
    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list.
        response = self.browser.get(self.live_server_url)
        self.item_input_box().send_keys('Buy wellies')
        self.item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')
        
        # She accidentally tries to enter a duplicate item.
        self.item_input_box().send_keys('Buy wellies')
        self.item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You've already got this in your list."
        ))

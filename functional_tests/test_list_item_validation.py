from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for_text('cannot be blank')

        # She tries again with some text for the item, which now works
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Trying again')
        inputbox.send_keys(Keys.ENTER)

        # Perversely, she now decides to submit a second blank list item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)
        
        # She receives a similar warning on the list page
        self.wait_for_text('cannot be blank')
        
        # And she can correct it by filling some text in
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('How about now?')
        inputbox.send_keys(Keys.ENTER)

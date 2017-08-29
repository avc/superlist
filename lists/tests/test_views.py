from django.test import TestCase
from lists.models import Item, List
from django.utils.html import escape

class HomePageTest(TestCase):
        
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        current_list = List.objects.create()
        response = self.client.get(f'/lists/{current_list.id}/')
        self.assertEquals(response.context['list'], current_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            f'/lists/{correct_list.id}/',
            data = {'item_text': 'A new item for an existing list'}
        )
        
        self.assertEquals(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEquals(item.text, 'A new item for an existing list')
        self.assertEquals(item.list, correct_list)
    
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data = {'item_text': 'A new item for an existing list'}
        )
        # Test that the URL is the same as the POST URL above, i.e. no redirect.
        self.assertEqual(response.status_code, 200)
    
class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new item')
        
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new item'})
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')
        
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item.")
        self.assertContains(response, expected_error)
        
    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_validation_errors_end_up_on_list_page(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data = {'item_text': ''}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item.")
        self.assertContains(response, expected_error)
        self.assertEqual(List.objects.count(), 2)
        self.assertEqual(Item.objects.count(), 0)
        
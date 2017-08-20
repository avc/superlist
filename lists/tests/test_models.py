from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

class ListAndItemModelsTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        # save 1st item
        first_item = Item()
        first_item.text = "The first (ever) item"
        first_item.list = list_
        first_item.save()
        
        # save 2nd item
        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        # get all items and count
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        # compare items equal to constants
        self.assertEqual(saved_items[0].text, 'The first (ever) item', )
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, 'Item the second')
        self.assertEqual(saved_items[1].list, list_)

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

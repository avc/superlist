from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

class ItemModelTest(TestCase):
    
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
    
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item(list=list_)
        item.save()
        self.assertIn(item, list_.item_set.all())
        
    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
        
    def test_list_ordering(self):
        list1 = List.objects.create()
        items = []
        for i in range(0, 3):
            items.append(Item.objects.create(list=list1, text=f'Item {i}'))
        self.assertEqual(list(Item.objects.all()), items)

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
        
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item.objects.create(list=list_, text='bla')
            item.full_clean()
    
    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item.objects.create(list=list2, text='bla')
        item.full_clean() # Should not raise.

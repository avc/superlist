from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_id}/')
    return render(request, 'list.html', {'list': list_})
    
def new_list(request):
    list_ = List.objects.create()
    try:
        item = Item.objects.create(text=request.POST['item_text'], list=list_)
        item.full_clean()
    except ValidationError:
        list_.delete()
        return render(request, 'home.html', {'error': "You can't have an empty list item."})
    return redirect(f'/lists/{list_.id}/')

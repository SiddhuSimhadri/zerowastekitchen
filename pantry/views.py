from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PantryItem
from .forms import PantryItemForm
from datetime import date, timedelta
import requests
from django.conf import settings

@login_required
def dashboard(request):
    user = request.user
    items = PantryItem.objects.filter(user=request.user, used=False).order_by('expiration_date')
    today = date.today()
    warning_date = today + timedelta(days=2)

    pantry_items = PantryItem.objects.filter(user=user).order_by('expiration_date')
    # Get ingredient names for API
    ingredient_names = ','.join(item.name for item in items)
    total_items = pantry_items.count()

    # Filter expired items
    expired_items = pantry_items.filter(expiration_date__lt=today).count()

    # Filter items expiring soon (within 3 days but not expired)
    expiring_soon = pantry_items.filter(expiration_date__gte=today, expiration_date__lte=warning_date).count()

    recipes = []
    if ingredient_names:
        try:
            url = 'https://api.spoonacular.com/recipes/findByIngredients'
            params = {
                'ingredients': ingredient_names,
                'number': 5,
                'ranking': 1,
                'apiKey': settings.SPOONACULAR_API_KEY,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            recipes = response.json()
        except Exception as e:
            print(f"Recipe API error: {e}")

    context = {
        'items': items,
        'warning_date': warning_date,
        'recipes': recipes,
        'total_items': total_items,
        'expired_items': expired_items,
        'expiring_soon': expiring_soon,
    }
    return render(request, 'pantry/dashboard.html', context)


@login_required
def add_pantry_item(request):
    if request.method == 'POST':
        form = PantryItemForm(request.POST)
        if form.is_valid():
            pantry_item = form.save(commit=False)
            pantry_item.user = request.user
            pantry_item.save()
            return redirect('dashboard')
    else:
        form = PantryItemForm()
    return render(request, 'pantry/add_pantry_item.html', {'form': form})

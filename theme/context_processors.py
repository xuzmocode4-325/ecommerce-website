# myapp/context_processors.py
from store.models import Category  # Import the necessary model

def categories_processor(request):
    categories = Category.objects.all()  # Fetch the categories
    return {'categories': categories}

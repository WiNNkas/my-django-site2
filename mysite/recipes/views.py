from django.shortcuts import render, redirect, get_object_or_404
from .models import ChefProfile, Recipe, Category, Comment, Like, Ingredient
from django.db.models import Q  # Импорт для сложного поиска

def index(request):
    error = ""
    if request.method == 'POST':
        name = request.POST.get('username')
        passw = request.POST.get('password')
        if ChefProfile.objects.filter(username=name, password=passw).exists():
            request.session['chef_name'] = name 
            return redirect('menu')
        error = "Неверный логин или пароль!"
    return render(request, 'index.html', {'error': error})

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        mail = request.POST.get('email')
        passw = request.POST.get('password')
        if ChefProfile.objects.filter(username=name).exists():
            return render(request, 'signup.html', {'error': 'Имя занято!'})
        ChefProfile.objects.create(username=name, email=mail, password=passw)
        request.session['chef_name'] = name
        return redirect('menu')
    return render(request, 'signup.html')

def menu_view(request):
    chef = request.session.get('chef_name')
    if not chef: return redirect('index')
    
    query = request.GET.get('q')
    cat_id = request.GET.get('category')
    recipes = Recipe.objects.all()
    
    if query:
        # 1. Приводим весь поисковый запрос к нижнему регистру и бьем на слова
        words = [word.lower() for word in query.split()]
        
        # 2. Получаем все рецепты из базы (для фильтрации в Python)
        all_recipes = Recipe.objects.all()
        
        # 3. Оставляем только те, где хотя бы одно слово совпадает (без учета регистра)
        filtered_ids = []
        for recipe in all_recipes:
            title_lower = recipe.title.lower() # Название рецепта в нижний регистр
            if any(word in title_lower for word in words):
                filtered_ids.append(recipe.id)
        
        # 4. Возвращаем QuerySet только с найденными ID
        recipes = Recipe.objects.filter(id__in=filtered_ids)
    
    if cat_id: 
        recipes = recipes.filter(category_id=cat_id)
    
    return render(request, 'menu.html', {
        'chef': chef, 
        'recipes': recipes, 
        'categories': Category.objects.all()
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    chef_name = request.session.get('chef_name')
    if request.method == 'POST' and chef_name:
        author = ChefProfile.objects.get(username=chef_name)
        Comment.objects.create(recipe=recipe, author=author, text=request.POST.get('text'))
        return redirect('recipe_detail', pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'chef': chef_name})

def toggle_like(request, pk):
    chef_name = request.session.get('chef_name')
    if not chef_name: return redirect('index')
    user = ChefProfile.objects.get(username=chef_name)
    recipe = get_object_or_404(Recipe, pk=pk)
    like_qs = Like.objects.filter(user=user, recipe=recipe)
    if like_qs.exists(): like_qs.delete()
    else: Like.objects.create(user=user, recipe=recipe)
    return redirect('menu')

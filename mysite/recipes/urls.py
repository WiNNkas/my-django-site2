from django.urls import path
from .views import *  

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup_view, name='signup'),
    path('menu/', menu_view, name='menu'), 
    path('menu/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('menu/<int:pk>/like/', toggle_like, name='toggle_like'),
]

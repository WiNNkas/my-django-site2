from django.db import models

class ChefProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100) 
    email = models.EmailField()

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [('easy', 'Легко'), ('medium', 'Средне'), ('hard', 'Сложно')]
    
    title = models.CharField(max_length=200, verbose_name="Название блюда")
    description = models.TextField(verbose_name="Описание приготовления")
    image = models.ImageField(upload_to='recipes/', verbose_name="Фото блюда", blank=True, null=True)
    author = models.ForeignKey(ChefProfile, on_delete=models.CASCADE, related_name='recipes', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    cooking_time = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients_list')
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(ChefProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(ChefProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    class Meta:
        unique_together = ('user', 'recipe')

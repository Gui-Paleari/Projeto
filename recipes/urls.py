from django.urls import path

from recipes import views

# Usado para quando der um nome a URL
# utiliza app_name para simplificar o atributo name logo a baixo de
# ex: name="recipes-home" para name="home"
# e depois coloca no template na url da tag "a" dessa forma -> recipes:home
app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/search/", views.search, name="search"),
    path(
        "recipes/category/<int:category_id>/", views.category, name="category"
    ),
    path("recipes/<int:id>/", views.recipe, name="recipe"),
]

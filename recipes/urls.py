from django.urls import path

from recipes import views

# Usado para quando der um nome a URL
# utiliza app_name para simplificar o atributo name logo a baixo de
# ex: name="recipes-home" para name="home"
# e depois coloca no template na url da tag "a" dessa forma -> recipes:home
app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path(
        "recipes/search/", views.RecipeListViewSearch.as_view(), name="search"
    ),
    path(
        "recipes/category/<int:category_id>/",
        views.RecipeListViewCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:pk>/", views.RecipeDetail.as_view(), name="recipe"),
]

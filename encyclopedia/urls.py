from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("404", views.error, name="error"),
    path("random", views.get_random, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit"),
]

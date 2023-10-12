from django.contrib import admin
from flix.models import Collection, Movie


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user", "uuid"]
    search_fields = ["title", "user__username", "uuid"]
    autocomplete_fields = ["user", "movies"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "genres", "uuid"]
    search_fields = ["title", "uuid"]

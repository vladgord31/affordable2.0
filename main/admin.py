from django.contrib import admin
from .models import Category, Movie, Genre, MovieShots, Actor, PaymentIntent, Rating, Comments, Reviews, Seat

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(MovieShots)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(Comments)
admin.site.register(Reviews)
admin.site.register(Seat)
admin.site.register(PaymentIntent)

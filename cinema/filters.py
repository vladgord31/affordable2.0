import django_filters
from main.models import Movie

class MovieFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='exact')
    movie_rating = django_filters.NumberFilter(field_name='movie_rating', lookup_expr='gte')
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")

    class Meta:
        model = Movie
        fields = ['genre', 'movie_rating', 'category',]

from django.urls import path
from cinema import views as cinema_views

app_name = "cinema"

urlpatterns = [
    path("search/", cinema_views.MovieCatalogView.as_view(), name="search"),
    path("", cinema_views.MovieCatalogView.as_view(), name="catalog"),
    path("movie/<slug:movie_slug>/", cinema_views.MovieDetailView.as_view(), name="movie"),
    path("comment/<slug:movie_slug>/", cinema_views.AddComment.as_view(), name="movie_comment"),
    path("review/<slug:movie_slug>/", cinema_views.AddReview.as_view(), name="movie_review"),
    path("tickets/", cinema_views.index, name="movie_tickets"),
    path('tickets/occupied/', cinema_views.occupiedSeats,name="occupied_seat"),
    path('tickets/payment/', cinema_views.makePayment,name="payment"),
]

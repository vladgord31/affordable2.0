import json
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
import requests 
from cinema.utils import q_search
from main.models import Category, Comments, Genre, Movie, MovieShots, PaymentIntent, Seat
from django.views.generic.base import View
from cinema.forms import CommentForm, ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import q_search
from django.views.decorators.csrf import csrf_exempt

class MovieCatalogView(View):
    def get(self, request):
        genres = Genre.objects.all()
        categories = Category.objects.all()
        movies = Movie.objects.all()

        genre_slug = request.GET.get('genre')
        category_slug = request.GET.get('category')
        query = request.GET.get('q')

        if category_slug:
            movies = Movie.objects.filter(category__slug=category_slug)
            movies = get_list_or_404(movies)
        elif query:
            movies = q_search(query)

        if genre_slug:
            movies = movies.filter(genres__slug=genre_slug)

        paginator = Paginator(movies, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'movies': page_obj,
            'genres': genres,
            'categories': categories,
            'genre_slug': genre_slug,
        }
        return render(request, 'cinema/catalog.html', context)

class MovieDetailView(View):
    def get(self, request, movie_slug):
        movie = get_object_or_404(Movie, slug=movie_slug)
        movies = Movie.objects.exclude(slug=movie_slug)[:4]
        comments = movie.comments.all()
        reviews = movie.reviews.all()
        review_form = ReviewForm()
        movieshots = MovieShots.objects.filter(movie=movie)
        context = {
            "movie": movie,
            "movies": movies,
            "comments": comments,
            "reviews": reviews,
            "review_form": review_form,
            "movieshots": movieshots,
        }
        return render(request, "cinema/movie.html", context)

class AddComment(LoginRequiredMixin, View):
    def post(self, request, movie_slug):
        form = CommentForm(request.POST)
        movie = get_object_or_404(Movie, slug=movie_slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
        return redirect("cinema:movie", movie_slug=movie_slug)

class AddReview(LoginRequiredMixin, View):
    def post(self, request, movie_slug):
        form = ReviewForm(request.POST)
        movie = get_object_or_404(Movie, slug=movie_slug)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user 
            review.save()
        return redirect("cinema:movie", movie_slug=movie_slug)


def index(request):
    movies = Movie.objects.all()
    return render(request, "cinema/tickets.html", {"movies": movies})


@csrf_exempt
def occupiedSeats(request):
    data = json.loads(request.body)

    movie = Movie.objects.get(title=data["movie_title"])
    occupied = movie.booked_seats.all()
    occupied_seat = list(map(lambda seat: seat.seat_no - 1, occupied))

    return JsonResponse({"occupied_seats": occupied_seat, "movie": str(movie)})


@csrf_exempt
def makePayment(request):
    data = json.loads(request.body)
    seat_numbers = list(map(lambda seat: seat + 1, data["seat_list"]))
    movie_title = data["movie_title"]

    cost = Movie.objects.get(title=movie_title).price

    header = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET}",
        "Content-Type": "application/json",
    }

    data = {
        "name": "Payment of Movie Ticket",
        "amount": int(cost * len(seat_numbers)) * 100,
        "description": f"Payment for {len(seat_numbers)} ticket(s) of {movie_title}",
        "collect_phone": True,
        "redirect_url": f"{settings.HOST_URL}/payment-confirm/",
    }

    response = requests.post("https://api.paystack.com/page", json=data, headers=header)

    if response.status_code == 200:
        response_data = response.json()
        slug = response_data["data"]["slug"]
        redirect_url = f"https://paystack.com/pay/{slug}"

        PaymentIntent.objects.create(
            referrer=redirect_url, movie_title=movie_title, seat_number=seat_numbers
        )

        return JsonResponse({"payment_url": redirect_url})

    return JsonResponse({"error": "Sorry, the payment service is not available at the moment."})

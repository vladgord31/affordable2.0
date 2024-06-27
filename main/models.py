from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Actor(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ім'я")
    age = models.PositiveSmallIntegerField(default=0, verbose_name="Вік")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    image = models.ImageField(upload_to="actors/", verbose_name="Зображення")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актори і режисери"
        verbose_name_plural = "Актори і режисери"


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"

class Seat(models.Model):
    seat_no = models.IntegerField(verbose_name="Номер місця")
    occupant_first_name = models.CharField(max_length=250, verbose_name="Ім'я")
    occupant_last_name = models.CharField(max_length=250, verbose_name="Прізвище")
    occupant_email = models.EmailField(max_length=50, verbose_name="Пошта")
    purchase_time = models.DateTimeField(default=timezone.now, verbose_name="Дата створення замрвлення:")

    def __str__(self) -> str:
        return f"{self.occupant_first_name}-{self.occupant_last_name} seat_no {self.seat_no}"

    class Meta:
        verbose_name = "Місце"
        verbose_name_plural = "Місця"

class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name="Назва фільму", unique=True)
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    age = models.PositiveSmallIntegerField(verbose_name="Обмеження у віці")
    year = models.DateField(default=timezone.now, verbose_name="Дата виходу")
    video = models.FileField(upload_to="main_video", verbose_name="Трейлер фільму")
    date = models.DateTimeField(default=timezone.now, verbose_name="Початок фільму")
    runtime = models.PositiveIntegerField(default=0, verbose_name="Тривалість фільму", help_text="Тривалість у хвилинах")
    poster = models.ImageField(upload_to="main_img", blank=True, null=True, verbose_name="Постер")
    img = models.ImageField(upload_to="main_img", blank=True, null=True, verbose_name="Прев'ю фільму")
    description = models.TextField(blank=True, null=True, verbose_name="Опис фільму")
    country = models.CharField(max_length=100, verbose_name="Країна")
    movie_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Рейтинг фільму")
    world_premiere = models.DateField(default=timezone.now, verbose_name="Світова прем'єра")
    budget = models.PositiveIntegerField(default=0, verbose_name="Бюджет", help_text="Вказувати суму в гривнях")
    draft = models.BooleanField(verbose_name="Чорновик", default=False)
    price = models.PositiveIntegerField(default=0, verbose_name="Ціна фільма", help_text="Вказувати ціну в гривнях")
    created = models.DateTimeField(auto_now_add=True, verbose_name="")

    booked_seats = models.ManyToManyField(Seat, blank=True, related_name="film_seats")
    directors = models.ManyToManyField(Actor, verbose_name="Режисер", related_name="film_directors")
    actors = models.ManyToManyField(Actor, verbose_name="Актор", related_name="film_actors")
    genres = models.ManyToManyField(Genre, verbose_name="Жанри", related_name="film_genres")
    category = models.ForeignKey(Category, verbose_name="Категорія", on_delete=models.SET_NULL, null=True, related_name="film_category")

    def __str__(self):
        return self.title

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0.0

    def get_absolute_url(self):
        return reverse("movie_detail", args=[self.slug])

    def display_id(self):
        return f"{self.id:05}"

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"


class PaymentIntent(models.Model):
    referrer = models.URLField(verbose_name="Посилання")
    movie_title = models.CharField(max_length=250, verbose_name="Назва фільма")
    seat_number = models.CharField(max_length=200, verbose_name="Номер місця")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплати"

class MovieShots(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    description = models.TextField(verbose_name="Опис")
    image = models.ImageField(verbose_name="Зображення", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр з фільма"
        verbose_name_plural = "Кадри з фільму"

class Rating(models.Model):
    ip = models.CharField(max_length=15, verbose_name="IP-адреса")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фільм", related_name="ratings")

    def __str__(self):
        return f"{self.ip} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Comments(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    text = models.TextField(max_length=5000, verbose_name="Повідомлення")
    parent = models.ForeignKey('self', verbose_name="Батько", on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата створення")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(verbose_name="Лайки", default=0)
    dislikes = models.PositiveIntegerField(verbose_name="Дизлайки", default=0)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"


class Reviews(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.TextField(max_length=5000, verbose_name="Повідомлення")
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.title} - {self.movie}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

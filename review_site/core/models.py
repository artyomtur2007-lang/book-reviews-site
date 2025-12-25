from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name='books')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 5 + 1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.rating}★"


from django.db import models

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    mobile = models.IntegerField(unique=True)


class Movie(models.Model):
    popularity = models.FloatField(default=0.0)
    director = models.CharField(max_length=256)
    genre = models.TextField()
    imdb_score = models.FloatField(default=0.0)
    name = models.CharField(max_length=256)


class UserSearchHistory(models.Model):
    mobile = models.IntegerField()
    movie_name = models.TextField()


class PhoneOTP(models.Model):
    mobile = models.IntegerField()
    otp = models.IntegerField()

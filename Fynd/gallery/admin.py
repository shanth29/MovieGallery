from django.contrib import admin
from . models import Customer, Movie, PhoneOTP, UserSearchHistory
# Register your models here.


class AdminCustomerView(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email', 'mobile']
    ordering = ['id']


class AdminMovieView(admin.ModelAdmin):
    list_display = ['id','popularity','director','genre','imdb_score', 'name']
    ordering = ['id']


class AdminMovieSearchView(admin.ModelAdmin):
    list_display = ['id','mobile','movie_name']
    ordering = ['id']


admin.site.register(Customer, AdminCustomerView)
admin.site.register(Movie, AdminMovieView)
admin.site.register(UserSearchHistory, AdminMovieSearchView)
admin.site.register(PhoneOTP)
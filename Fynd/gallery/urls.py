from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('',views.get_home),
    path('adminLogin',views.admin_login),
    path('adminLogout',views.admin_logout),
    path('loadData',views.load_data),
    path('listMovie',views.get_movies_list),
    path('movieDetails',views.get_movie_details),
    path('searchMovie',views.get_movie_searched),
    path('customerSignup',views.customer_registration),
    path('loginOtp',views.customer_login),
    path('loginCustomer',views.validate_login),
    path('addMovie',views.add_movies),
    path('editMovie',views.edit_movies),
    path('deleteMovie',views.delete_movies),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import Customer, Movie, PhoneOTP, UserSearchHistory
from . serializers import CustomerSerializer, MovieSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from . functions import send_otp
import json


@api_view()
def get_home(request):
    """
        Test API
        Request Type: GET
    """
    return Response({"Welcome": "To Fynd!"})


@api_view(['POST'])
def admin_login(request):
    """
        Admin Login API:
        Request Type: POST
        Input: username, password
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password = password)
        try:
            if user.is_staff:
                login(request, user)
                return Response({"message":"Admin Logged In Successfully"}, status= status.HTTP_201_CREATED)
            else:
                return Response({"alert":"Invalid Login"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def admin_logout(request):
    """
        Admin Logout API:
        Request Type: GET
    """
    if request.method == 'GET':
        logout(request)
        return Response({"message":"Admin Logout Successfully"}, status= status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def load_data(request):
    """
        API To add/map Json file data to Database:
        Request Type: POST
        Input: username, password (admin credentials)
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            try:
                with open('static/imdb.json','r') as fread:
                    data = json.load(fread)
                for i in data:
                    popularity = i.get('99popularity')
                    director = i.get('director')
                    genre = i.get('genre')
                    imdb_score = i.get('imdb_score')
                    name = i.get('name')
                    if Movie.objects.filter(name = name):
                        pass
                    else:
                        Movie.objects.create(popularity = popularity, director = director, genre = genre, imdb_score = imdb_score, name = name)
                return Response({"message":"Done With Adding Data To Database"}, status= status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'alert':'User Is Not An Admin'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view()
def get_movies_list(request):
    """
        API To View ALL Movies Name for All type of Users:
        Request Type: GET
        Output : All Movies Name along with Id
    """
    if request.method == 'GET':
        movie_data = Movie.objects.values_list('id','name', named=True).all()
        return Response(movie_data)


@api_view(['POST'])
def get_movie_details(request):
    """
        API TO Get Passed Movie Details:
        Request Type: Post
        Input : Movie Name
        Output : Movie Details
    """
    if request.method == 'POST':
        name = request.data.get('name')
        try:
            if Movie.objects.filter(name = name):
                movie_data = Movie.objects.filter(name = name).all()
                movie_data = MovieSerializer(movie_data, many =True)
                return Response(movie_data.data)
            return Response({name:'Entered Movie Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e},status = status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_movie_searched(request):
    """
        API To Search Desired Movie:
        Request Type: Post
        Input : Movie Name
        Output : Post messege regarding presence of Movie Entry in Database
    """
    if request.method == 'POST':
        try:
            if 'mobile' in request.data and 'movie_name' in request.data:
                mobile = request.data.get('mobile')
                name = request.data.get('movie_name')
                if Customer.objects.filter(mobile = mobile):
                    if Movie.objects.filter(name = name):
                        if UserSearchHistory.objects.filter(mobile = mobile):
                            get_data = UserSearchHistory.objects.select_for_update().get(mobile = mobile)
                            get_data.movie_name = get_data.movie_name +", "+name
                            get_data.save() 
                            return Response({name:'Entered Movie Is Present In List'},status=status.HTTP_201_CREATED)
                        else:
                            UserSearchHistory.objects.create(mobile = mobile, movie_name = name)
                            return Response({name:'Entered Movie Is Present In List'},status=status.HTTP_201_CREATED)
                    return Response({name:'Entered Movie Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({mobile:'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'movie_name' in request.data:
                name = request.data.get('movie_name')
                if Movie.objects.filter(name = name):
                    return Response({name:'Entered Movie Is Present In List'},status=status.HTTP_201_CREATED)
                return Response({name:'Entered Movie Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'alert': 'Entered Data Miss Matched'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e},status = status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def customer_registration(request):
    """
        API To Signup:
        Request Type: Post
        Input : First_Name, Last_Name, Email, Mobile
        Output : Message regarding status
    """
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'User Created Succesfully'},status=status.HTTP_201_CREATED)
            return Response({'alert':'User Already Registered'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def customer_login(request):
    """
        API To get OTP:
        Request Type: Post
        Input : Mobile
        Output : Get Otp for verification
    """
    if request.method == 'POST':
        mobile = str(request.data.get('mobile'))
        try:
            if Customer.objects.filter(mobile = mobile):
                get_otp = send_otp(mobile)
                if get_otp:
                    PhoneOTP.objects.create(mobile = mobile, otp = get_otp)
                    return Response({'OTP':get_otp},status=status.HTTP_201_CREATED)
                return Response({'alert':'OTP Not Generated'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'alert':'Users Mobile Number Is Not Registered'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def validate_login(request):
    """
        API To Login:
        Request Type: Post
        Input : Mobile, OTP
        Output : Message regarding Status
    """
    if request.method == 'POST':
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        try:
            if mobile and otp:
                if PhoneOTP.objects.filter(mobile = mobile, otp = otp):
                    PhoneOTP.objects.filter(mobile = mobile, otp = otp).delete()
                    return Response({'success':'You Have Logged In'},status=status.HTTP_201_CREATED)
                return Response({'alert':'User Have Entered Wrong OTP'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'alert':'User Have Not Entered OTP Or Mobile Number'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_movies(request):
    """
        API To Add New Movies:
        Request Type: Post
        Input : Scheme in Json format of New Record
        Output : Message regarding Status
    """
    if request.method == 'POST':
        try:
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Movie Added Succesfully'},status=status.HTTP_201_CREATED)
            return Response({'alert':'Input Provided Was Incorrect'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_movies(request):
    """
        API To Edit Movie Record:
        Request Type: Post
        Input : Scheme in Json Format With Required Changes in Previous Record
        Output : Message Regarding Status
    """
    if request.method == 'PUT':
        try:
            if 'id' in request.data:
                id = request.data.get('id')
                previous_data = Movie.objects.values_list(named=True).all().get(id =id)
                if Movie.objects.filter(id = id):
                    if 'popularity' in request.data:
                        previous_popularity = previous_data.popularity
                        popularity = request.data.get('popularity')
                        Movie.objects.filter(popularity=previous_popularity).update(popularity=popularity)
                    else:
                        pass
                    if 'director' in request.data:
                        previous_director = previous_data.director
                        director = request.data.get('director')
                        Movie.objects.filter(director=previous_director).update(director=director)
                    else:
                        pass
                    if 'genre' in request.data:
                        previous_genre = previous_data.genre
                        genre = request.data.get('genre')
                        Movie.objects.filter(genre=previous_genre).update(genre=genre)
                    else:
                        pass
                    if 'imdb_score' in request.data:
                        previous_imdb_score= previous_data.imdb_score
                        imdb_score = request.data.get('imdb_score')
                        Movie.objects.filter(imdb_score=previous_imdb_score).update(imdb_score=imdb_score)
                    else:
                        pass
                    if 'name' in request.data:
                        previous_name = previous_data.name
                        name = request.data.get('name')
                        Movie.objects.filter(name=previous_name).update(name=name)
                    else:
                        pass
                    return Response({'message':'Movie Records Updated succesfully'},status=status.HTTP_201_CREATED)
                return Response({'alert':'Movie ID Does Not Exist'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'alert':'Primary Key Not Present In Request'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_movies(request):
    """
        API To Delete Movie Record:
        Request Type: Post
        Input : Movie Name
        Output : Message Regarding Status
    """
    if request.method == 'DELETE':
        name = request.data.get('movie_name')
        try:
            if Movie.objects.filter(name=name):
                Movie.objects.filter(name = name).delete()
                return Response({'message':'Movie Deleted Succesfully'},status=status.HTTP_201_CREATED)
            return Response({'alert':'Input Provided Was Incorrect'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Exception':e}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'alert':'Error In Request'},status=status.HTTP_400_BAD_REQUEST)
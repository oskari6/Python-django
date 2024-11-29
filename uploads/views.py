from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from uploads.forms import UploadForm
from uploads.models import Movie
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import boto3
from .models import Drink
from .serializers import DrinkSerializer

def home(request):
    return HttpResponse("ok")

def movies(request):
    data = Movie.objects.all()
    return render(request, 'movies/movies.html', {'movies': data})

def movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)

    if movie is not None:
        return render(request, 'movies/movie.html', {'movie': movie})
    else:
        raise Http404('Movie does not exist')

def detail(request, id):
    data = Movie.objects.get(pk=id)
    return render(request, 'movies/detail.html', {'movie': data})


def add(request):
    title = request.POST.get('title')#[] works also but throws error if first time and no data
    year = request.POST.get('year')

    if title and year:
        movie = Movie(title=title, year=year)
        movie.save()
        return HttpResponseRedirect('/movies')
    
    return render(request, 'movies/add.html')

def upload(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
        return redirect(home)
    return render(request, 'movies/upload.html', {'form': UploadForm})
            
def delete(request, id):
    try:
        movie = Movie.objects.get(pk=id)
    except:
        raise Http404('Movie does not exist')
    movie.delete()
    return HttpResponseRedirect('/movies')

@api_view(['GET', 'POST'])
def drinks(request):
    db = boto3.resource("dynamodb")
    table = db.Table("drinks")

    if request.method == 'GET':
        drinks = table.scan()
        return Response({"drinks": drinks.get("Items")})
    elif request.method == 'POST':
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
        except: 
            return Response({"error": "Failed to insert"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(["GET", "PUT", "DELETE"])
def drink(request, name):
    db = boto3.resource("dynamodb")
    table = db.Table("drinks")

    if request.method == "GET":
        drink = table.get_item(Key={
            "name": name
        })

        if (drink.get("Item") is not None):
            return Response({"drink": drink.get("Item")})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "PUT":
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({"error":"Failed to update"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "DELETE":
        table.delete_item(Key={
            "name": name
        })
        return Response(status=status.HTTP_200_OK)
    

#decorator
@api_view(['GET', 'POST'])
def drink_list(request, format=None):
    #get all the drinks
    #serialize them
    #return json
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id, format=None):

    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
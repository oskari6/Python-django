from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from uploads.forms import UploadForm
from uploads.models import Movie

def home(request):
    return render(request, "home/home.html")

def movies(request):
    data = Movie.objects.all()
    return render(request, 'movies/movies.html', {'movies': data})

def movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)

    if movie is not None:
        return render(request, 'movies/movie.html', {'movie': movie})
    else:
        raise Http404('Movie does not exist')

def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        image = request.FILES.get('image')

        if title and year and image:
            movie = Movie(title=title, year=year, image=image)
            movie.save()
            return redirect('/movies/')  # Redirect to the movies page
        
        return HttpResponse("All fields are required.", status=400)

    return render(request, 'movies/add.html')
    
def delete(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        movie.delete()
    except:
        raise Http404('Movie does not exist')
    return redirect('/movies/')
from django.shortcuts import render,get_object_or_404
from user.models import Movie
from app1.models import User_reg
from django.db.models import Q
# Create your views here.


def search_result(request):
    movies=None
    query=None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movies = Movie.objects.all().filter(Q(title__contains=query) | Q(description__contains=query))
        return render(request, 'search.html', {'movies': movies, 'query': query})

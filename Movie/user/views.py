from django.shortcuts import render, redirect, reverse, get_object_or_404
from app1.models import User_reg
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import Movie,Categories,ReviewRatings
from django.contrib.auth.decorators import login_required


@login_required(login_url='/app1/login/')
def home(request, c_slug=None):
    current_user = request.user
    c_page = None
    movie_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Categories, slug=c_slug)
        movie_list = Movie.objects.filter(categories=c_page).order_by('-id')
    else:
        movie_list = Movie.objects.all().order_by('-id')

    paginator = Paginator(movie_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'category': c_page, 'movies': movies,'user':current_user})


@login_required(login_url='/app1/login/')
def home_movie_detail(request,c_slug,m_slug):
    current_user = request.user
    try:
        movies=Movie.objects.get(categories__slug=c_slug,slug=m_slug)
    except Exception as e:
        raise e

    has_rated = ReviewRatings.objects.filter(user=current_user, movie=movies).exists()

    rr = ReviewRatings.objects.filter(movie=movies)

    rr_list = []
    total_rating = 0
    num_ratings = 0
    for i in rr:
        total_rating += i.rating
        num_ratings += 1

        rr_list.append({
            'user': i.user,
            'review': i.review,
            'rating': i.rating,
            })

    if num_ratings != 0:
        average_rating = total_rating / num_ratings
    else:
        average_rating = 'NA'

    if request.method == 'POST':

        if has_rated:
            message='You have already rated and reviewed this movie'
            return render(request, 'home_movie_detail.html',{'movie': movies, 'user': current_user,'message':message,'rr':rr, 'rating':average_rating})
        else:
            review = request.POST.get('review')
            rating = request.POST.get('rating')

            ReviewRatings.objects.create(user=current_user,movie=movies,review=review,rating=rating)

            return redirect(reverse('user:home_movie_detail', args=[movies.categories.slug, movies.slug]))

    return render(request, 'home_movie_detail.html', {'movie': movies, 'user': current_user, 'rr': rr_list, 'rating': average_rating})

@login_required(login_url='/app1/login/')
def movie_detail(request,c_slug,m_slug):
    current_user = request.user
    try:
        movies=Movie.objects.get(categories__slug=c_slug,slug=m_slug)
    except Exception as e:
        raise e

    rr = ReviewRatings.objects.filter(movie=movies)

    rr_list = []
    total_rating = 0
    num_ratings = 0
    for i in rr:
        total_rating += i.rating
        num_ratings += 1

        rr_list.append({
            'user': i.user,
            'review': i.review,
            'rating': i.rating,
        })

    if num_ratings != 0:
        average_rating = total_rating / num_ratings
    else:
        average_rating = 'NA'
    return render(request,'movie_detail.html',{'movie': movies, 'user':current_user,'rr': rr_list, 'rating': average_rating})


@login_required(login_url='/app1/login/')
def profile(request):
    current_user = request.user
    return render(request, 'profile.html', {'user': current_user})


def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        current_user.username = username
        current_user.first_name = firstname
        current_user.last_name = lastname
        current_user.email = email
        current_user.save()
        return redirect('user:profile')
    return render(request, 'edit_profile.html', {'user': current_user})


@login_required(login_url='/app1/login/')
def add_movies(request):
    current_user = request.user

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('desc')
        date = request.POST.get('date')
        actors = request.POST.get('actors')
        link = request.POST.get('link')
        category = request.POST.get('category')
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None

        collections={'user': current_user,'title':title,'description':description,'date':date,'actors':actors,'link':link,'category':category}

        if not title:
            errors = 'Please enter a movie title.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})
        if not description:
            errors= 'Please provide a movie description.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})
        if not date:
            errors= 'Please specify the movie release date.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})
        if not actors:
            errors= 'Please enter the movie actors.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})
        if not link:
            errors = 'Please provide a link for the movie.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})
        if not category:
            errors = 'Please select a movie category.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})
        if not image:
            errors = 'Please upload a movie image.'
            return render(request, 'add_movies.html', {'errors': errors, **collections})

        try:
            category_slug = slugify(category)
            category, created = Categories.objects.get_or_create(name=category, slug=category_slug)
        except Categories.DoesNotExist:
            return render(request, 'add_movies.html', {'user': current_user, 'error': 'Category does not exist.'})

        slug = slugify(title)
        counter = 1
        while Movie.objects.filter(slug=slug).exists():
            slug = f"{slug}-{counter}"
            counter += 1

        movie = Movie(
            user=current_user,
            title=title,
            slug=slug,
            description=description,
            release_date=date,
            actors=actors,
            link=link,
            categories=category,
            image=image
        )
        movie.save()
        return redirect('user:your_movies')

    return render(request, 'add_movies.html', {'user': current_user})

@login_required(login_url='/app1/login/')
def your_movies(request):
    current_user = request.user
    movie_list = Movie.objects.filter(user=current_user)

    paginator = Paginator(movie_list,6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)

    context = {
        'movies': movies,
        'user': current_user

    }
    return render(request, 'profile.html',context)

@login_required(login_url='/app1/login/')
def edit_movie(request, c_slug, m_slug):
    current_user = request.user
    movie = get_object_or_404(Movie, categories__slug=c_slug, slug=m_slug)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('desc')
        date = request.POST.get('date')
        actors = request.POST.get('actors')
        link = request.POST.get('link')
        category_name = request.POST.get('category')
        image = request.FILES.get('image')

        category_slug = slugify(category_name)
        category, created = Categories.objects.get_or_create(name=category_name, slug=category_slug)

        movie.title = title
        movie.description = description
        movie.release_date = date
        movie.actors = actors
        movie.link = link
        movie.categories = category
        movie.slug = slugify(title)

        if image:
            movie.image = image
        movie.save()

        return redirect(reverse('user:movie_detail', args=[movie.categories.slug, movie.slug]))

    return render(request, 'edit_movie.html', {'movie': movie, 'user': current_user})


@login_required(login_url='/app1/login/')
def delete(request,c_slug,m_slug):
    current_user = request.user
    movie = get_object_or_404(Movie, user__username=current_user, slug=m_slug, categories__slug=c_slug)
    if request.method == 'POST':

        movie.delete()
        return redirect('user:your_movies')
    return render(request,'delete.html',{'movie':movie})



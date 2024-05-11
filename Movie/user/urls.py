from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('home/',views.home,name='home'),
    # path('home/<str:username>/', views.home, name='home_user'),
    path('home/<str:c_slug>/', views.home,name='all_movies'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_movies/', views.add_movies, name='add_movies'),
    path('your_movies/', views.your_movies, name='your_movies'),
    path('movie_detail/<str:c_slug>/<str:m_slug>/',views.movie_detail,name='movie_detail'),
    path('<str:c_slug>/<str:m_slug>/',views.home_movie_detail,name='home_movie_detail'),
    path('edit_movie/<str:c_slug>/<str:m_slug>/',views.edit_movie,name='edit_movie'),
    path('delete/<str:c_slug>/<str:m_slug>/',views.delete,name='delete'),
]

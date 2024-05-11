from django.contrib import admin
from .models import Movie,Categories,ReviewRatings

# Register your models here.

admin.site.register(Movie)
admin.site.register(Categories)
admin.site.register(ReviewRatings)



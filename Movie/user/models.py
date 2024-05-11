from django.db import models
from django.urls import reverse
from app1.models import User_reg


class Categories(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('user:all_movies', args=[self.slug])


class Movie(models.Model):
    user = models.ForeignKey(User_reg, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    link = models.URLField(max_length=300)
    categories = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='movie_images/', null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('user:movie_detail', kwargs={'c_slug': self.categories.slug, 'm_slug': self.slug})


class ReviewRatings(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User_reg, on_delete=models.SET_NULL, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return str(self.movie)

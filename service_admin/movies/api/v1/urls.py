from django.urls import include, path
from movies.api.v1 import views

urlpatterns = [
    
    path(
        "movies?<int:page>",
        views.MoviesListApi.as_view(),
        name="movies-by-page"
    ),
    path("movies/<uuid:pk>", views.MoviesDetailApi.as_view(), name="movies-by-pk"),
    path('movies', views.MoviesListApi.as_view(), name="movies"),
]

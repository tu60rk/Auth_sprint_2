from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import FilmWork


class MoviesApiMixin:
    paginate_by = 50
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        film_works = (
            self.model.objects
            .prefetch_related("all_genres", "all_persons")
            .annotate(genres=ArrayAgg('all_genres__name', distinct=True))
            .annotate(directors=ArrayAgg('all_persons__full_name', distinct=True, filter=Q(personfilmwork__role="director")))
            .annotate(writers=ArrayAgg('all_persons__full_name', distinct=True, filter=Q(personfilmwork__role="writer")))
            .annotate(actors=ArrayAgg('all_persons__full_name', distinct=True, filter=Q(personfilmwork__role="actor")))
        )
        return film_works
    
    def render_to_response(self, context):
        return JsonResponse(context)

    def get(self, request, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)

class MoviesListApi(MoviesApiMixin, BaseListView):
    def get_context_data(self, request, **kwargs):
        queryset = self.get_queryset()

        if request.GET.get('pages', None):
            paginator = Paginator(queryset, per_page = self.paginate_by)
            page = paginator.get_page(int(request.GET.get('pages')))
            queryset = page.object_list
        else:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, 
                self.paginate_by
            )
        context = {
                "count": paginator.count ,
                "total_pages": paginator.num_pages,
                "prev": page.previous_page_number() if page.has_previous() else None,
                "next": page.next_page_number() if page.has_next() else None,
                'results': list(queryset.values("id", "title", "description", "creation_date", "rating", "type", "genres", "directors", "writers", "actors"))
        }
        return context

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, request, **kwargs):
        queryset = self.get_queryset()
        context = queryset.filter(id=kwargs.get('pk')).values("id", "title", "description", "creation_date", "rating", "type", "genres", "directors", "writers", "actors")
        return  context[0]

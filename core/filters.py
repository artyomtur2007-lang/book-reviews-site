import django_filters
from django.db.models import Q
from .models import Book, Genre

class ContentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_search_query',
        label="Поиск по названию"
    )

    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        field_name='genres',
        label="Жанры"
    )

    year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='exact',
        label="Год выпуска"
    )

    def filter_by_search_query(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )

    class Meta:
        model = Book
        fields = ['search', 'year', 'genres']
from django.forms import DateInput
from django_filters import FilterSet, CharFilter, \
    ModelMultipleChoiceFilter, DateFilter, \
    ModelChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author, Category


# создаём фильтр
class PostFilter(FilterSet):
    title = CharFilter('title',
                       label='Заголовок содержит:',
                       lookup_expr='icontains',
                       )

    postCategory = ModelChoiceFilter(field_name='postCategory',
                               label='Категория:',
                               lookup_expr='exact',
                               queryset=Category.objects.all()
                               )

    datetime = DateFilter(
        field_name='dateCreation',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Даты позже'
    )

    class Meta:
        model = Post
        fields = []

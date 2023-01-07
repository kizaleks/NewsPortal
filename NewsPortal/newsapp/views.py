from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category,Author
from datetime import datetime
from .filters import PostFilter
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect

class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
class PostForm(forms.ModelForm):
    # postCategory = forms.ModelMultipleChoiceField(
    #     label='Категория',
    #     # queryset=Category.objects.all(),
    # )

    class Meta:
        model = Post
        fields = ['title','text','postCategory']


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'add.html'
    success_url = '/news'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author=Author.objects.get(authorUser=self.request.user)
        post.categoryType = 'NW'

        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'add.html'
    success_url = '/news'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author.authorUser = User.first_name
        post.categoryType = 'AR'
        return super().form_valid(form)
# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post',)
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# дженерик для удаления товара

class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'delete_post.html'
    queryset = Post.objects.all
    context_object_name = 'new'
    success_url = '/news'
    success_url = reverse_lazy('/news')
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        if not hasattr(user, 'author'):
            Author.objects.create(
                authorUser=User.objects.get(pk=user.id)
            )
    return redirect('/news')

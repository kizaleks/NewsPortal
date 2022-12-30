from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate,ArticleCreate, PostDeleteView, PostUpdateView

urlpatterns = [
        path('news', PostList.as_view(), name='news'),
        path('news/create', NewsCreate.as_view(), name='post_create_nw'),
        path('news/<int:pk>', PostDetail.as_view(),name='post_detail_nw'),
        path('news/<int:pk>/edit', PostUpdateView.as_view(),name='post_update_nw'),
        path('news/<int:pk>/delete', PostDeleteView.as_view(),name='post_delete_nw'),
        path('news/search', PostSearch.as_view(),name='post_search'),
        path('articles/create', ArticleCreate.as_view(), name='post_create_article'),
        path('articles/<int:pk>', PostDetail.as_view(),name='post_detail_articles'),
        path('articles/<int:pk>/edit', PostUpdateView.as_view(),name='post_update_articles'),
        path('articles/<int:pk>/delete', PostDeleteView.as_view(),name='post_delete_articles'),

]
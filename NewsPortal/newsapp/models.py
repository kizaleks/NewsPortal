from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
#Класс Автор
class Author(models.Model):
    authorUser=models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor= models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser}'

    def update_rating(self):
        rate_post_author = self.post_set.all().aggregate(sum_rating=Sum('rating') * 3)['sum_rating']
        rate_comment = self.authorUser.comment_set.all().aggregate(sum_rating=Sum('rating'))['sum_rating']
        rate_comment_post = Post.objects.filter(author=self).values('rating')  # в ответ список querry_set , проходим циклом и складываем сумму рейтинга всех комментариев ко всем post автора.
        a = 0
        for i in range(len(rate_comment_post)): a = a + rate_comment_post[i]['rating']
        self.rate = rate_post_author + rate_comment + a
        self.save()

#Класс Категории
class Category(models.Model):
    name=models.CharField(max_length=64, unique=True)
    subscribers=models.ManyToManyField(User, related_name='category')
    def __str__(self):
        return f'{self.name}'

#Класс Пост
class Post(models.Model):
    author= models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS='NW'
    ARTICLE='AR'
    CATEGORY_CHOICES=(
        (NEWS,'Новость'),
        (ARTICLE,'Статья')
    )
    categoryType=models.CharField(max_length=2, choices=CATEGORY_CHOICES,default=ARTICLE)
    dateCreation=models.DateTimeField(auto_now_add=True)
    postCategory=models.ManyToManyField(Category, through='PostCategory')
    title=models.CharField(max_length=128)
    text=models.TextField()
    rating=models.SmallIntegerField(default=0)
    # def __str__(self):
    #     return f'{self.postCategory}'


    def like(self):
        self.rating +=1
        self.save()
        # Author.authorUser.
        # self.author
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'
    def __str__(self):
        return f'{self.title} | {self.author}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

#Класс Категории постов
class PostCategory(models.Model):
    postThrough=models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough=models.ForeignKey(Category,on_delete=models.CASCADE)

# Класс Коментарии
class Comment(models.Model):
    commentPost=models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    dateCreation=models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
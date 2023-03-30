from .models import Post, Category,Author
from modeltranslation.translator import register, TranslationOptions
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Post)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'text','postCategory' )
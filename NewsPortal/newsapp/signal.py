from django.db.models.signals import m2m_changed
from django.dispatch import  receiver
from .models import PostCategory
from .tasks import notfy_about_new_post

@receiver(m2m_changed,  sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add' and instance.__class__.__name__ == 'Post':
        notfy_about_new_post.delay(
            instance.id, instance.title, instance.text,
        )


from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from hlis.category.models import Category
from hlis.custom_auth.models import ApplicationUser
from hlis.utils.utils import get_post_path


class Post(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name='user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    caption = models.TextField(_('caption'), null=True, blank=True)
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)


    class Meta:
        verbose_name = _('Post')

    def __str__(self):
        return f'{self.id}{self.caption}'


class PostFile(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_file')
    post_file = models.FileField(upload_to=get_post_path, null=True, blank=True)

    class Meta:
        verbose_name = _('Post File')

    def __str__(self):
        return str(self.post)


class Tag(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tag')
    user_tag = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Tag User')

    def __str__(self):
        return str(self.post)


class HashTag(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_hashtag')
    user_hashtag = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Hash Tag')

    def __str__(self):
        return str(self.post)


class Comments(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_details')
    comment = models.CharField(_('Comment'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Comment')

    def __str__(self):
        return f'{self.id}'


class Likes(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(_('Like'), default=False)

    class Meta:
        verbose_name = _('Like')

    def __str__(self):
        return f'{self.id}'

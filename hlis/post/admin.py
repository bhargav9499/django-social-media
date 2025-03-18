from django.contrib import admin
from hlis.post.models import Post, PostFile, Tag, HashTag, Likes


class HashTagInline(admin.TabularInline):
    model = HashTag
    extra = 1


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (PostFileInline, TagInline, HashTagInline)


admin.site.register(Tag)
admin.site.register(Likes)

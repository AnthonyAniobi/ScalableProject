from django.contrib import admin
from .models import ImageModel, Photo, Like, Comment


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'uploaded_at')
    list_filter = ('path', 'uploaded_at')
    search_fields = ('title', 'path')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption_preview', 'created_at', 'like_count', 'comment_count')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'caption')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'photo__caption')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content', 'photo__caption')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

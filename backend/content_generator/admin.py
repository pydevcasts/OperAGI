from django.contrib import admin

from .models import AnalyticsSnapshot, GeneratedContent, Post, Schedule


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'platform', 'language', 'status', 'created_at')
    list_filter = ('platform', 'language', 'status')
    search_fields = ('user__email', 'content')


@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    list_display = ('post', 'provider', 'generated_at', 'updated_at')
    search_fields = ('post__user__email', 'generated_text', 'title')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('post', 'scheduled_for', 'timezone', 'status', 'processed_at')
    list_filter = ('status', 'timezone')


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'reach', 'likes', 'captured_at')
    list_filter = ('platform',)

from django.contrib import admin
from .models import Post, GeneratedContent 


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'platform', 'status', 'created_at', 'updated_at')
    list_filter = ('platform', 'status', 'created_at', 'updated_at')
    search_fields = ('content', 'visual_idea', 'user__username') # جستجو بر اساس محتوا، ایده بصری و نام کاربری
    list_editable = ('status',) # اجازه تغییر وضعیت از لیست ادمین
    readonly_fields = ('created_at', 'updated_at', 'published_at') # این فیلدها فقط خواندنی باشند


    fieldsets = (
        (None, {
            'fields': ('user', 'platform', 'content', 'visual_idea')
        }),
        ('Advanced options', {
            'classes': ('collapse',), # این بخش در ابتدا بسته است
            'fields': ('status', 'created_at', 'updated_at', 'published_at'),
        }),
    )

class GeneratedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'content_type', 'generated_at')
    list_filter = ('content_type', 'generated_at')
    search_fields = ('generated_text', 'suggested_hashtags', 'post__user__username') # جستجو بر اساس متن تولید شده، هشتگ‌ها و نام کاربری کاربر مرتبط با پست
    readonly_fields = ('generated_at', 'post') # فیلد post را فقط خواندنی می‌کنیم چون از طریق relation انتخاب می‌شود

    # --- برای جلوگیری از ایجاد چندین GeneratedContent برای یک Post ---
    def has_add_permission(self, request):
        if request.method == 'GET' and request.path.endswith('/add/'):
             pass
        return super().has_add_permission(request)

    # --- نمایش فیلدهای مرتبط با Post در صفحه ادمین GeneratedContent ---
    fieldsets = (
        ('Main Content', {
            'fields': ('post', 'content_type', 'generated_text', 'suggested_hashtags')
        }),
        ('Scheduling & Advanced', {
            'classes': ('collapse',),
            'fields': ('suggested_publish_time', 'generated_at', 'avatar_video_url', 'audio_file_path'),
        }),
    )


# --- (اختیاری) تعریف Inline برای نمایش GeneratedContent در صفحه Post ---
class GeneratedContentInline(admin.StackedInline): # یا admin.TabularInline
    model = GeneratedContent
    can_delete = False # معمولا نمی‌خواهیم GeneratedContent را مستقیماً از صفحه Post حذف کنیم
    extra = 0 # صفر معنی‌اش این است که هیچ فرم اضافه‌ای برای اضافه کردن جدید نمایش داده نمی‌شود
    readonly_fields = ('generated_at', 'content_type') # فیلدهای فقط خواندنی در اینلاین


class PostAdminWithInline(PostAdmin):
    inlines = [GeneratedContentInline]


admin.site.register(Post, PostAdminWithInline)
admin.site.register(GeneratedContent, GeneratedContentAdmin)


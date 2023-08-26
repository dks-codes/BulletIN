from django.contrib import admin
from news.models import Category,News, Comment, NewsType, Plan, PlanFeatures

from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

# class NewsAdmin(admin.ModelAdmin):

class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('category', 'headline','report_by', 'date')
    search_fields = ('report_by','date')
    list_filter = ('category', 'date')
    list_editable = ('headline',)
    filter_horizontal = ('news_type',)

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('comment','created_on')
#     # search_fields = ('is_visible', 'User.username')

class PlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('feature',)

admin.site.register(Category)
admin.site.register(News,NewsAdmin)
admin.site.register(Comment)
admin.site.register(NewsType)
admin.site.register(Plan,PlanAdmin)
admin.site.register(PlanFeatures)


from django.contrib import admin
from news.models import Category,News, Comment, NewsType, Plan, PlanFeatures

from django_summernote.admin import SummernoteModelAdmin

#to see session in admin panel
import pprint
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
class SessionAdmin(admin.ModelAdmin):
    def user(self, obj):
        session_user = obj.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=session_user)
        return user.email
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags = True
    list_display = ['user', 'session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    
admin.site.register(Session,SessionAdmin)
#########


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





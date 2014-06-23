from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lsp2.submissions.models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(Vote, admin.ModelAdmin)
admin.site.register(License, admin.ModelAdmin)
admin.site.register(Mime, admin.ModelAdmin)
admin.site.register(File, admin.ModelAdmin)
admin.site.register(Submission, admin.ModelAdmin)
admin.site.register(ProjectSubmission, admin.ModelAdmin)
admin.site.register(SampleSubmission, admin.ModelAdmin)
admin.site.register(ThemeSubmission, admin.ModelAdmin)

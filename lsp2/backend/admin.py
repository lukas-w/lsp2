from django.contrib import admin

from lsp2.backend.models import *


admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(Vote, admin.ModelAdmin)
admin.site.register(License, admin.ModelAdmin)
admin.site.register(Mime, admin.ModelAdmin)
admin.site.register(File, admin.ModelAdmin)
admin.site.register(Submission, admin.ModelAdmin)
admin.site.register(ProjectSubmission, admin.ModelAdmin)
admin.site.register(SampleSubmission, admin.ModelAdmin)
admin.site.register(ThemeSubmission, admin.ModelAdmin)

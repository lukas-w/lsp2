from django.contrib import admin

from lsp2.backend.models import *


admin.site.register(PlatformUser, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Subcategory, admin.ModelAdmin)
admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(Rating, admin.ModelAdmin)
admin.site.register(License, admin.ModelAdmin)
admin.site.register(AllowedMime, admin.ModelAdmin)
admin.site.register(File, admin.ModelAdmin)
admin.site.register(Submission, admin.ModelAdmin)


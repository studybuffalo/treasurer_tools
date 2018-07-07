from django.contrib import admin

from .models import Branch, BranchMember

class BranchAdmin(admin.ModelAdmin):
    pass

class BranchMemberAdmin(admin.ModelAdmin):
    list_display = ("branch", "user")
    list_filter = ("branch", "user")
    ordering = ("branch", "user")

# Register the sites
admin.site.register(Branch, BranchAdmin)
admin.site.register(BranchMember, BranchMemberAdmin)

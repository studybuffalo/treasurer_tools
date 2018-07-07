from django.contrib import admin

from .models import Branch, BranchMember

class BranchAdmin(admin.ModelAdmin):
    pass

class BranchMemberAdmin(admin.ModelAdmin):
    pass

# Register the sites
admin.site.register(Branch, BranchAdmin)
admin.site.register(BranchMember, BranchMemberAdmin)

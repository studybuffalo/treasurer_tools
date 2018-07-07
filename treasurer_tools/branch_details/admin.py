from django.contrib import admin

from .models import BranchMember

class BranchMemberAdmin(admin.ModelAdmin):
    pass

# Register the sites
admin.site.register(BranchMember, BranchMemberAdmin)

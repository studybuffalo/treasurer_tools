"""General views for the Django application"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def account_profile(request):
    """The user profile page"""
    return render(
        request,
        "account/profile.html",
        context={},
    )

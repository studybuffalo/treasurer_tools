"""Views for the reports app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

@login_required
def dashboard(request):
    """Main dashboard to manage payees and payers"""
    return render(
        request,
        "reports/index.html",
        context={},
    )

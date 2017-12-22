from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Demographics


# Create your views here.
@login_required
def dashboard(request):
    """Main dashboard to manage payees and payers"""
    return render(
        request,
        "payee_payer/index.html",
        context={},
    )

class RequestPayeePayers(LoginRequiredMixin, generic.ListView):
    model = Demographics

    context_object_name = "payee_payer_list"
    template_name = "payee_payer/payee_payer_list.html"
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def dashboard(request):
    """Main dashboard to manage payees and payers"""
    return render(
        request,
        "payee_payer/index.html",
        context={},
    )
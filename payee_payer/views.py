from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .models import Demographics
from .forms import PayeePayerForm

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
    
@login_required
def add_payee_payer(request):
    """Generates and processes form to add a new payee/payer"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer_data = Demographics()

        # Create a form instance and populate it with data from the request (binding):
        form = PayeePayerForm(request.POST, instance=payee_payer_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            name = form.cleaned_data["name"]
            
            # Upate the user settings
            # payee_payer_data.name = name
            

            # payee_payer_data.save()

            # redirect to a new URL:
            messages.success(request, "Payee/payer successfully added")

            return HttpResponseRedirect(reverse("payee_payer_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = PayeePayerForm(initial={})

    return render(
        request, 
        "payee_payer/add.html", 
        {'form': form}
    )
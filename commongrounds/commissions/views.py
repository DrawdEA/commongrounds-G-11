from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView 
from .models import Commission
from .forms import CommissionForm
# Create your views here.


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'

class CommissionCreateView(CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_form.html"
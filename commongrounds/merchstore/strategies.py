from django.shortcuts import redirect
from django.urls import reverse

from .models import Transaction


class BaseTransactionStrategy:
    def execute(self, request, product, form):
        raise NotImplementedError


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction = form.save(commit=False)
        transaction.product = product
        transaction.buyer = request.user.profile
        transaction.save()
        return redirect('merchstore:cart')


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session['pending_transaction'] = {
            'product_pk': product.pk,
            'amount': form.cleaned_data['amount'],
        }
        login_url = reverse('login')
        next_url = reverse('merchstore:product_detail', args=[product.pk])
        return redirect(f'{login_url}?next={next_url}')

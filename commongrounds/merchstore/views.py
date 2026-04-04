from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Transaction
from .forms import ProductForm, TransactionForm


def product_list(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        my_products = Product.objects.filter(owner=profile)
        other_products = Product.objects.exclude(owner=profile)
    else:
        my_products = Product.objects.none()
        other_products = Product.objects.all()
    return render(request, 'merchstore/product_list.html', {
        'my_products': my_products,
        'other_products': other_products,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_owner = request.user.is_authenticated and product.owner == request.user.profile
    form = TransactionForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.buyer = request.user.profile
            transaction.save()
            product.stock = max(0, product.stock - transaction.amount)
            if product.stock == 0:
                product.status = Product.Status.OUT_OF_STOCK
            product.save()
            return redirect('merchstore:cart')
    return render(request, 'merchstore/product_detail.html', {
        'product': product,
        'form': form,
        'is_owner': is_owner,
    })


@login_required
def product_create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.profile
            product.save()
            return redirect('merchstore:product_detail', pk=product.pk)
    return render(request, 'merchstore/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user.profile:
        return redirect('merchstore:product_list')
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.stock == 0:
                updated.status = Product.Status.OUT_OF_STOCK
            else:
                updated.status = Product.Status.AVAILABLE
            updated.save()
            return redirect('merchstore:product_detail', pk=pk)
    return render(request, 'merchstore/product_form.html', {'form': form, 'product': product})


@login_required
def cart_view(request):
    transactions = Transaction.objects.filter(
        buyer=request.user.profile
    ).select_related('product__owner')

    grouped = {}
    for t in transactions:
        owner = t.product.owner
        grouped.setdefault(owner, []).append(t)

    return render(request, 'merchstore/cart.html', {'grouped': grouped.items()})


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(
        product__owner=request.user.profile
    ).select_related('buyer')

    grouped = {}
    for t in transactions:
        buyer = t.buyer
        grouped.setdefault(buyer, []).append(t)

    return render(request, 'merchstore/transaction_list.html', {'grouped': grouped.items()})

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Sum
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from .forms import ProductForm, UserRegisterForm
from .models import Product

def register(request):
    if request.user.is_authenticated:
        return redirect("inventory:dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully.",
            )

            return redirect("inventory:dashboard")
    else:
        form = UserRegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()

            messages.success(
                request,
                "Product created successfully.",
            )

            return redirect("inventory:product_list")
    else:
        form = ProductForm()

    context = {
        "form": form,
        "page_title": "Add Product",
    }

    return render(
        request,
        "inventory/product_form.html",
        context,
    )


@login_required
def dashboard(request):
    products = Product.objects.filter(owner=request.user)

    context = {
        "total_products": products.count(),
        "total_stock": products.aggregate(
            total=Sum("quantity")
        )["total"] or 0,
        "low_stock_products": products.filter(
            quantity__lte=F("low_stock_threshold")
        ).count(),
        "recent_products": products[:5],
    }

    return render(
        request,
        "inventory/dashboard.html",
        context,
    )


@login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user)

    query = request.GET.get("q", "").strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(sku__icontains=query)
        )

    context = {
        "products": products,
        "query": query,
    }

    return render(
        request,
        "inventory/product_list.html",
        context,
    )

@login_required
def product_edit(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Product updated successfully.",
            )

            return redirect("inventory:product_list")
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "page_title": "Edit Product",
    }

    return render(
        request,
        "inventory/product_form.html",
        context,
    )
    

@login_required
def product_delete(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":
        product.delete()

        messages.success(
            request,
            "Product deleted successfully.",
        )

        return redirect("inventory:product_list")

    return render(
        request,
        "inventory/product_confirm_delete.html",
        {"product": product},
    )
    

"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import ProductForm, ReviewForm
from .models import *


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class AccountPageView(TemplateView):
    template_name = 'account.html'

class WomenPageView(ListView):
    template_name = 'women.html'
    model = Product

class MenPageView(ListView):
    template_name = 'men.html'
    model = Product

class DecorationsPageView(ListView):
    template_name = 'decorations.html'
    model = Product

class AccessoriesPageView(ListView):
    template_name = 'accessories.html'
    model = Product

class ContactPageView(TemplateView):
    template_name = 'contact.html'
    model = Product

class OrderSuccessPageView(TemplateView):
    template_name = 'ordersuccess.html'

def cart(request):
    # check if user is logged in
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False) # find the order that the current user has not completed
                                                                                        # otherwise, create a new order
    # if not log in, user cannot add into cart, so total price always 0
    else:
        order = {'get_cart_total':0}

    context = {'object':order}
    return render(request, 'cart.html', context)

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                customer= request.user,
                body=form.cleaned_data["body"],
                product=product,
            )
            review.save()
    context = {"product": product, "reviews": reviews, "form": form}
    return render(request, "product_detail.html", context)

@login_required
# add to cart functionality
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk) # checking if there is a product with this primary key (PK)
    order_item, create = OrderItem.objects.get_or_create(product=item, customer=request.user, complete=False) # create this product as an order item (if already is an order item, only get)
    order_qs = Order.objects.filter(customer=request.user, complete=False)  # find the uncompleted order that is made by this particular user 
    if order_qs.exists():
        # if there is such an order and the product exists, add it into cart
        # if the order item was already in the cart, only add the quantity to the existing order item
        order = order_qs[0]
        if order.items.filter(product__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
        # if the order item was not in the cart, add it in
        else:
            order.items.add(order_item)

    # create a new order then add the item in if there is no uncompleted order before
    else:
        order = Order.objects.create(customer=request.user)
        order.items.add(order_item)
    return redirect("products:product_details", pk=pk) # redirect to the item detail page


@login_required
# remove from cart functionality
def remove_one_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk) # checking if there is a product with this primary key (PK)
    order_qs = Order.objects.filter(customer=request.user, complete=False) # find the uncompleted order that is made by this particular user 
    if order_qs.exists():
        # if there is such an order and the product exists, find out whether the product is in the cart
        order = order_qs[0]
        if order.items.filter(product__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(product=item, customer=request.user, complete=False)[0] # locate the item in the order
            # decrease the order item quantity by 1 if there are more than 1 of this product in the cart
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            # completely remove this order item if there is only 1 of this product
            else:
                order.items.remove(order_item)
                order_item.delete()
        else:
            pass

    return redirect("products:cart")


@login_required
# remove from cart functionality
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk) # checking if there is a product with this primary key (PK)
    order_qs = Order.objects.filter(customer=request.user, complete=False) # find the uncompleted order that is made by this particular user 
    if order_qs.exists():
        # if there is such an order and the product exists, find out whether the product is in the cart
        order = order_qs[0]
        if order.items.filter(product__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(product=item, customer=request.user, complete=False)[0] # locate the item in the order
            # decrease the order item quantity by 1 if there are more than 1 of this product in the cart
            if order_item.quantity >= 1:
                order.items.remove(order_item)
                order_item.delete()
        else:
            pass

    return redirect("products:cart")

def checkout(request):
    order = Order.objects.get(customer=request.user, complete=False)
    order_items = order.items.all()
    order_items.update(complete=True)
    for item in order_items:
        item.save()

    order.complete = True
    order.save()

    return redirect("products:ordersuccess")



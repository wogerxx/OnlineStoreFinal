from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from environ import Env

from .models import Product, Cart, Category

env = Env()
env.read_env()

User = get_user_model()



class ProductsView(ListView):
    template_name = "app_main/index.html"
    model = Product
    paginate_by = 6
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        page_obj = context['page_obj']
        left_index = page_obj.number - 2
        right_index = page_obj.number + 2
        
        if left_index < 1:
            left_index = 1
        
        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        
        return context

class CategoryView(ListView):
    template_name = "app_main/categories.html"
    model = Category
    paginate_by = 6
    context_object_name = "categories"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        page_obj = context['page_obj']
        left_index = page_obj.number - 2
        right_index = page_obj.number + 2
        
        if left_index < 1:
            left_index = 1
        
        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "app_main/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = 'product_id'

class CartView(ListView):
    template_name = 'app_main/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return self.request.user.cart_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        total_price = sum(item.total_price for item in cart_items)
        context['total_price'] = total_price
        return context


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'app_main/category_detail.html', {'category': category, 'products': products})



@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))  

        try:

            cart_item = Cart.objects.get(product=product, user=request.user)

            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f"Added {quantity} {product.name}(s) to your cart.")
        except Cart.DoesNotExist:

            Cart.objects.create(
                product=product,
                user=request.user,
                quantity=quantity
            )
            messages.success(request, f"Added {quantity} {product.name}(s) to your cart.")

    return redirect('cart')



@login_required(login_url='login')
def change_cart_product_quantity(request, cart_product_id, action):
    cart_product = get_object_or_404(Cart, id=cart_product_id)

    if action == "increment":
        cart_product.quantity += 1
    elif action == "decrement" and cart_product.quantity > 1:
        cart_product.quantity -= 1
    else:
        cart_product.delete()

    cart_product.save()
    return redirect('cart')

def checkout(request):
    # Fetch all cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return HttpResponse("No items in your cart.")
    
    # Calculate the total price and generate the list of product names
    products = [item.product for item in cart_items]
    total_price = sum(item.product.new_price * item.quantity for item in cart_items)

    data = f'Your ordered items: {", ".join([product.name for product in products])} and total price is {total_price + 10}'

    if request.method == 'POST':
        to_email = request.user.email
        subject = 'Your Ordered Items From Our Store'
        body = f"<html><body>{data}</body></html>" 

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        username = env('EMAIL_HOST_USER')
        password = env('EMAIL_HOST_PASSWORD')

        from_email = 'Muhammadamin Miraimov <muhammadmiraimov11@gmail.com>'

        msg = MIMEMultipart()
        msg['from'] = from_email
        msg['to'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(username, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            print('Email sent successfully')
        except Exception as e:
            print(f'Failed to send email. Error: {e}')
        finally:
            server.quit()
            cart_items.delete()

        return HttpResponse('Email sent!')


def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'app_main/index.html', {
        'products': products,
        'query': query,
    })


def remove_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            item = Cart.objects.get(user=request.user, product_id=product_id)
            item.delete()
            return redirect('cart')
        except Cart.DoesNotExist:
            return redirect('cart')

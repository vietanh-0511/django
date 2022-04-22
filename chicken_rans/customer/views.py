from django.db import reset_queries
from django.shortcuts import redirect, render
from .models import Category, Product,Customer,Order,Order_detail
import hashlib
from django.urls import reverse
# Create your views here.


def index(request):
    if 'customer' in request.session:
        customer_email = request.session['customer']
        category = Category.objects.all()
        product = Product.objects.all()
        context = {
            "category": category,
            "product": product,
            "customer": customer_email,
        }
        # dữ liệu đc đưa vào phải là dictionary{}
        return render(request, "customer\index.html", context)
    else:
        return redirect('login_view')

def category(request, id):
    if 'customer' in request.session:
        customer_email = request.session['customer']
        category = Category.objects.all()
        category_choosen = Category.objects.filter(id=id)
        product = Product.objects.filter(category=id)
        context = {
            "category": category,
            "category_choosen":category_choosen,
            "product": product,
            "customer": customer_email,
        }
        # dữ liệu đc đưa vào phải là dictionary{}
        return render(request, "customer\search_category.html", context)
    else:
        return redirect('login_view')

def search_view(request):
    if 'customer' in request.session:
        customer_email = request.session['customer']
        if request.method == "POST":
            search = request.POST['search']
            result = Product.objects.filter(name_product__contains=search)
            category = Category.objects.all()
            context = {
                "category": category,
                "customer": customer_email,
                'search': search,
                'chicken': result,
                'category':category
        }
    return render(request, "customer/search.html",context)

def register_view(request):
    if 'customer' in request.session:
        return redirect('index')

    return render(request, 'customer\\register.html')

def register_process(request):
    customer = Customer() 
    customer.first_name = request.POST.get('first_name')
    customer.last_name = request.POST.get('last_name')
    customer.email = request.POST.get('email')
    password = request.POST.get('password')
    customer.password = hashlib.md5(password.encode()).hexdigest()
    customer.save()
    return redirect('index')

def login_view(request):
    if 'customer' in request.session:
        return redirect('index')

    context = {}
    if request.GET.get('error'):
        context = {'error': 'Wrong email or password'}
    return render(request, 'customer\\login.html', context)

def login_process(request):
    if request.method == "POST":

        # nhận dữ liệu đã post
        email = request.POST.get("email")
        password = request.POST.get("password")
        # mã hóa md5 password
        password_hash_md5 = hashlib.md5(password.encode()).hexdigest()
        customer_check = Customer.objects.filter(
            email=email, password=password_hash_md5)
        if customer_check:
            request.session["customer"] = email
            return redirect('index')
        url = f"{reverse('login_view')}?error=true"
        return redirect(url)

    else:
        return redirect('login_view')

def logout(request):
    if 'customer' in request.session:
        del request.session['customer']
        return redirect('login_view')
    return redirect('login_view')

def get_total(order_detail):
    total = 0
    for item in order_detail:
        total += item.get_price()
    return total
    
def add_to_cart(request, id,):
    if 'customer' in request.session:
        email = request.session['customer']
        if request.method == "POST":
            product = Product.objects.get(id=id)
            quantity = request.POST.get("quantity")
            order = Order.objects.last()
            order_detail = Order_detail.objects.filter(
                order=order,
                product=product)

            if order.is_ordered == True:
                customer = Customer.objects.get(email=email)
                order = Order()
                order.customer = customer
                order.save()
        
            if order_detail:
                order_detail.update(quantity=quantity)

            else:
                order_detail = Order_detail()
                order_detail.order = order
                order_detail.product = product
                order_detail.price = product.price
                order_detail.quantity = quantity
                order_detail.save()

    return redirect('index')

def cart_view(request):
    if 'customer' in request.session:
        customer_email = request.session['customer']
        customer = Customer.objects.get(email=customer_email)
        order = Order.objects.filter(is_ordered=False, customer=customer)
        order_detail = Order_detail.objects.filter(order=order)
        order_detail = []
        
        if order:
            order_detail = Order_detail.objects.filter(order=order.first())

        context = {
            "customer": customer_email,
            "order_detail": order_detail,
            "total": get_total(order_detail),
        }
    return render(request, 'customer\cart.html', context)

def update_qty(request, id):
        if request.method == "POST":
            product = Product.objects.get(id=id)
            quantity = request.POST.get("quantity")
            order = Order.objects.last()
            order_detail = Order_detail.objects.filter(
                order=order,
                product=product)
            order_detail.update(quantity=quantity)
            return redirect('cart')

def remove(request, id):
    product = Product.objects.get(id=id)
    order = Order.objects.last()
    order_detail = Order_detail.objects.filter(
        order=order,
        product=product)
    order_detail.delete()
    return redirect('cart')

def checkout_form(request):
    if 'customer' in request.session:
        customer_email = request.session['customer']
        context = {
            "customer": customer_email,
        }
    return render(request, 'customer\checkout_form.html', context)
    
def checkout_process(request):
    name_customer = request.POST.get('full_name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    note = request.POST.get('note')
    if 'customer' in request.session:
        email = request.session['customer']
        customer = Customer.objects.get(email=email)
        order = Order.objects.filter(customer=customer)
        order.update(name_customer=name_customer,
                     phone_number=phone,
                     address=address,
                     notes=note,
                     is_ordered=True)
        print('phone')
    return redirect('index')

# def inc_qty(request, id):
    #         product = Product.objects.get(id=id)
#         order = Order.objects.last()
#         order_detail = Order_detail.objects.filter(
#             order=order,
#             product=product)
#         quantity = order_detail.first().quantity + 1
#         order_detail.update(quantity=quantity)
#         return redirect('cart')

# def dec_qty(request, id):
#         product = Product.objects.get(id=id)
#         order = Order.objects.last()
#         order_detail = Order_detail.objects.filter(
#             order=order,
#             product=product)
#         quantity = order_detail.first().quantity - 1
#         order_detail.update(quantity=quantity)
#         if quantity == 0:
#             order_detail.delete()
#         return redirect('cart')
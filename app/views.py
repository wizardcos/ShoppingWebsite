from django.shortcuts import render, redirect
from django.views import View
from .models import Product, CustomerAddress,Cart,Purchase# Import the CustomerAddress model
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
def home(request):
    return render(request, "app/home.html")


def about(request):
    return render(request, "app/about.html")


def contact(request):
    return render(request, "app/contact.html")


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())


class ProductDetails(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
            return redirect("customerregistration")
        else:
            messages.warning(request, "Invalid Data")
            return render(request, "app/customerregistration.html", locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            address =form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            reg = CustomerAddress(user=user,address=address, name=name, mobile=mobile, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save successfully.")
            return redirect("profile")  # Redirect to the profile page after successful form submission
        else:
            messages.warning(request, "Invalid Data")
        return render(request, "app/profile.html", locals())


class AddressView(View):
    def get(self, request):
        add= CustomerAddress.objects.filter(user=request.user)
        return render(request, "app/address.html", locals())
    

class Checkout(View):
    def get(self, request):
        user = request.user
        addresses = CustomerAddress.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount += value
        totalamount = amount + 40
        return render(request, "app/checkout.html", locals())

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_amount = 0

        # Assuming each user has a Customer object associated
        customer_address = CustomerAddress.objects.get(user=user)

        # Calculate the total amount and store the order for each item in the cart
        for item in cart_items:
            total_amount += item.product.selling_price * item.quantity
            Purchase.objects.create(
                user=user,
                customer=customer_address,
                product=item.product,
                quantity=item.quantity
            )

        # Clear the cart after placing the order
        cart_items.delete()

        # Show a success message
        messages.success(request, "Order placed successfully!")

        return redirect('checkout') 
    


def add_to_cart(request):
    if request.user.is_authenticated:
        try:
            user = request.user
            product_id = request.GET.get('prod_id')
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product).save()
            return redirect("/cart")
        except Product.DoesNotExist:
            return redirect("/cart")  # Redirect to a custom error page or handle the error accordingly
    else:
        return redirect("/login")  

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = get_object_or_404(Cart, product__id=prod_id, user=request.user)
        c.quantity += 1
        c.save()

        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount += value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = get_object_or_404(Cart, product__id=prod_id, user=request.user)
        c.quantity -= 1
        if c.quantity < 1:
            c.delete()
        else:
            c.save()

        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount += value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = get_object_or_404(Cart, product__id=prod_id, user=request.user)
        c.delete()

        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount += value
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

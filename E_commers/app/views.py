from django.shortcuts import render,redirect
from .models import Product,Categories,Filter_price,Color,Brand,Contact_us,Order
from  django.conf import settings
from  django.core.mail import send_mail
from  django.contrib.auth.models import User
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.conf import settings
from .models import *
from django.http import JsonResponse
import stripe
from django.views import View
from .forms import PaymentForm


import stripe




# Create your views here.
def Baseview(request):
    return render(request,"Main/base.html")

def Homeview(request):
    product =Product.objects.filter(status = 'Publish')
    context = {
        'product':product,
    }

    return render(request,"Main/index.html",context)

def Productview(request):

    categories = Categories.objects.all()
    filter_price = Filter_price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get("filter_price")
    COLOR_ID = request.GET.get('color')
    BRAND_ID = request.GET.get('brand')
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGH=request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW= request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')


    if CATID:
        product = Product.objects.filter(categories=CATID,status="Publish")
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price= PRICE_FILTER_ID,status="Publish")
    elif COLOR_ID:
        product = Product.objects.filter(color=COLOR_ID,status="Publish")
    elif BRAND_ID:
        product = Product.objects.filter(brand=BRAND_ID,status="Publish")
    elif ATOZID:
        product = Product.objects.filter(status="Publish").order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status="Publish").order_by('-name')
    elif PRICE_LOWTOHIGH:
        product = Product.objects.filter(status="Publish").order_by('price')
    elif   PRICE_HIGHTOLOW:
        product = Product.objects.filter(status="Publish").order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status="Publish",condition="New").order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status="Publish",condition="Old").order_by('-id')





    else:
        product = Product.objects.filter(status='Publish')


    context = {
        'product': product,
        'categories':categories,
        'filter_price': filter_price,
        'color':color,
        'brand':brand,


    }
    return render(request,"Main/product.html",context)

def Search(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)

    context = {
        'product': product,


    }


    return render(request,"Main/search.html",context)

def Product_Detail_Page(request,id):
    prod = Product.objects.filter(id=id).first()

    context = {
        'prod': prod,

    }

    return render(request,"Main/product_single.html",context)


def Contact_Page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact_us(
            name =name,
            email = email,
            subject = subject,
            message = message,
        )
        subject=subject
        message=message
        email_from=settings.EMAIL_HOST_USER
        recipient_list = [email]
        try:
            send_mail(subject,message,email_from, recipient_list)
            contact.save()
            return redirect("/a1/home/")
        except:
            return redirect("/a1/contact/")
    return render(request,"Main/contact.html",)






def HandleRegister(request):
    if request.method == "POST":
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email =request.POST.get("email")
        pass1=request.POST.get("pass1")
        pass2 =request.POST.get("pass2")

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name=first_name
        customer.last_name = last_name
        customer.save()
        return redirect("/a1/register/")

    return render(request, "Registration/auth.html", )

def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/a1/home/")
        else:
            return redirect("/a1/login/")


    return render(request, "Registration/auth.html", )


def HandleLogout(request):
    logout(request)
    return redirect("/a1/home/")
    return render(request, "Registration/auth.html", )



@login_required(login_url="/a1/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/a1/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/a1/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/a1/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/a1/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/a1/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_detail.html')

@login_required(login_url="/a1/login/")
def wishlist(request):
    return render(request, 'Cart/wishlist.html')




def Check_out(request):

    return render(request,"Cart/checkout.html")

# views.py
def Place_Order(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')

        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        country = request.POST.get("country")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        amount = request.POST.get("amount")




        user = request.user if request.user.is_authenticated else None


        order = Order(
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            user=user,


        )
        order.save()
        for i in cart:
            a = int(cart[i]['price'])
            b= cart[i]['quantity']
            total= a*b

            item=OrderItem(
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total



            )
            item.save()



    return render(request, 'Cart/placeorder.html')


def Success(request):
    return render(request,"Cart/thank-you.html")



from django.shortcuts import render
from datetime import datetime

def about(request):
    return render(request, 'Main/about.html', {
        'company_name': "HMART",
        'product_description': "Electronic products",
        'product_category': "Electronic",
        'year': 2024,
        'founder_name': "Kalyani",
        'starting_location': "New York",
        'motivation': "sustainable Ecomers",
        'niche': "eco-friendly products",
        'support_email': "kalyanigawande@gmail.com",
        'phone': "+1 234 567 890",
        'current_year': datetime.now().year
    })





stripe.api_key = settings.STRIPE_SECRET_KEY  # Ensure this is set correctly

# views.py
print("Stripe Secret Key:", settings.STRIPE_SECRET_KEY)  # Debugging line


class PaymentView(View):
    def get(self, request):
        form = PaymentForm()
        return render(request, 'Cart/payment.html', {'form': form, 'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = int(form.cleaned_data['amount'] * 100)  # Amount in cents
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                # Create a charge
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    description='Payment Description',
                    source=request.POST['stripeToken'],
                )
                return redirect('/a1/thank-you.html')  # Redirect to a success page
            except stripe.error.StripeError:
                return render(request, 'Cart/payment.html', {'form': form, 'error': 'Payment failed'})
        return render(request, 'Cart/payment.html', {'form': form})




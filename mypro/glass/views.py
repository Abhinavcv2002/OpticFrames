from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def index(request):
    product = Product.objects.all()
    return render(request, 'user/index.html', {'product': product})

def eyeglass(request):
    product = Product.objects.all()
    return render(request, 'user/eyeglass.html', {'product' : product})

def sunglass(request):
    product = Product.objects.all()
    return render(request, 'user/sunglass.html', {'product' : product})

def userin(request):
    if request.user.is_authenticated:
        return redirect('index')
    username = None
    password = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if not username or not password:
            messages.error(request, "Both username and password are required!")
            return render(request, 'user/userin.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'user/userin.html')

def userup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        print(username, password)

        if not username or not email or not password or not confirmpassword:
            messages.error(request,'all fields are required.')

        elif confirmpassword != password:
            messages.error(request,"password doesnot match")
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'user/userup.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff=True  
            user.save()
            messages.success(request,"account created successfully")
            return render(request, "user/userin.html")
    return render(request, 'user/userup.html')

def user_logout_view(request):
    logout(request)
    return render(request, 'user/userin.html')

def cart(request):
    return render(request, 'user/cart.html')

def product_details(request):
    return render(request, 'user/product_details.html')

def lenses_page(request):
    return render(request, 'user/lenses_page.html')

def home(request):
    return render(request, 'adminpage/home.html')

def adminin(request):
    if request.user.is_authenticated:
        return redirect('adminadd')
    username = None
    password = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if not username or not password:
            messages.error(request, "Both username and password are required!")
            return render(request, 'adminpage/adminin.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            return redirect('adminadd')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'adminpage/adminin.html')

def adminup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        print(username, password)

        if not username or not email or not password or not confirmpassword:
            messages.error(request,'all fields are required.')

        elif confirmpassword != password:
            messages.error(request,"password doesnot match")
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'adminpage/adminup.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff=True  
            user.save()
            messages.success(request,"account created successfully")
            return render(request, "adminpage/adminin.html")
    return render(request, 'adminpage/adminup.html')

def adminadd(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        description = request.POST.get('description')

        if not name or not price or not  image or not description:
            messages.error(request, "All fields are required!")
            return render(request, 'adminpage/adminadd.html')
        else:
            product = Product(name=name, price=price,  image=image,  description=description)
            product = Product(
            name=name, 
            price=price, 
            image=image, 
            description=description
        )
            product.save()
            messages.success(request, "Product added successfully!")
            return render(request, 'adminpage/adminadd.html', {'product': product})
    return render(request, 'adminpage/adminadd.html')


def admin_logout_view(request):
    logout(request)
    return render(request, 'adminpage/adminin.html')

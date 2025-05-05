from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.

def index(request):
    product = Product.objects.all()
    return render(request, 'user/index.html', {'product': product})

def men(request):
    product = Product.objects.all()
    return render(request, 'user/men.html', {'product' : product})

def women(request):
    product = Product.objects.all()
    return render(request, 'user/women.html', {'product' : product})

def userin(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            if  user.is_superuser:
                return redirect('adminhome')
            else:
                return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")
    
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

def signout(request):
    logout(request)
    request.session.flush()
    return redirect('index')

def cart(request, product_id):
    """
    Add a product to the cart by product_id.
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        if not request.user.is_authenticated:
            messages.error(request, "You must log in to add items to cart.")
            return redirect('userin')  # Redirect to custom login view

        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.totalprice = cart_item.quantity * product.price
            cart_item.save()
            messages.success(request, f"{product.name} quantity updated in your cart")
        else:
            Cart.objects.create(
                user=request.user,
                product=product,
                quantity=1,
                totalprice=product.price
            )
            messages.success(request, f"{product.name} added to your cart")

    return redirect('view_cart')  # Redirect to cart view
    
    # If not POST, redirect to cart as a fallback
    return redirect('cart')

def view_cart(request):
    """
    View the current user's cart.
    """
    if not request.user.is_authenticated:
        messages.warning(request, "Login to view your cart.")
        return redirect('userin')

    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum(item.totalprice for item in cart_items)
    # Example: assuming 10% discount for each item (you can customize logic)
    total_discount = sum((item.product.price * item.quantity * 0.10) for item in cart_items)
    total_payable = total_price - total_discount

    return render(request, 'user/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_discount': total_discount,
        'total_payable': total_payable,
        'cart_count': cart_items.count()
    })

# Add this function for removing items from cart
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart.
    """
    if not request.user.is_authenticated:
        return redirect('userin')
    
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f"{product_name} removed from your cart.")
    return redirect('view_cart')

# Add this function for updating cart quantities
def update_cart(request, item_id, action):
    """
    Update cart item quantity.
    """
    if not request.user.is_authenticated:
        return redirect('userin')
    
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            # If quantity becomes 0, remove the item
            return redirect('remove_from_cart', item_id=item_id)
    
    cart_item.totalprice = cart_item.quantity * cart_item.product.price
    cart_item.save()
    
    return redirect('view_cart')

# Add a placeholder checkout view
def checkout(request):
    """Process checkout."""
    if not request.user.is_authenticated:
        return redirect('userin')
    
    # Get cart items for the current user
    # This is just an example - adjust based on your actual cart model
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate cart totals
    cart_total = sum(item.get_total() for item in cart_items)
    shipping_cost = 5.00  # Example fixed shipping cost
    order_total = cart_total + shipping_cost
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': shipping_cost,
        'order_total': order_total,
    }
    
    # Process form submission for checkout
    if request.method == 'POST':
        # Handle the form submission - save order details, process payment, etc.
        # This is a simplified example
        order = Order.objects.create(
            user=request.user,
            total_amount=order_total,
            # Add more fields as needed
        )
        
        # Create order items from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
        
        # Clear the user's cart
        cart_items.delete()
        
        # Redirect to a success page
        return redirect('order_success', order_id=order.id)
    
    return render(request, 'user/checkout.html', context)

def product_details(request, pk):
    """
    View function for displaying product details.
    
    Args:
        request: The HTTP request object
        pk: The ID of the product to display
        
    Returns:
        Rendered product details page with product data
    """
    # Get the product by ID or return 404 if not found
    product = get_object_or_404(Product, id=pk)
    
    # Get all images for this product - ensure we only add images that exist
    images = []
    if product.image:
        images.append(product.image)
    if product.image1:
        images.append(product.image1)
    if product.image2:
        images.append(product.image2)
    if product.image3:
        images.append(product.image3)
    if product.image4:
        images.append(product.image4)
    if product.image5:
        images.append(product.image5)
    
    # If no images were found, use a placeholder or default image
    if not images:
        # You might want to set a default image here
        pass
    
    # Default values for non-authenticated users
    cart_product_ids = []
    cart_item_count = 0
    
    # Get cart information for authenticated users
    if request.user.is_authenticated:
        # Fetch cart items for the authenticated user
        cart_items = Cart.objects.filter(user=request.user)
        
        # Extract product IDs from the cart
        cart_product_ids = list(cart_items.values_list('product_id', flat=True))
        cart_item_count = cart_items.count()
    
    # Get related products (same category)
    related_products = []
    if hasattr(product, 'category') and product.category:
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=pk)[:4]  # Get 4 related products
    
    # Prepare the context to pass to the template
    context = {
        'product': product,
        'images': images,
        'cart_product_ids': cart_product_ids,
        'cart_item_count': cart_item_count,
        'page_title': f"{product.name} - OPTICFRAMES",
        'first_image': images[0] if images else None,
        'related_products': related_products,
    }
    
    return render(request, 'user/product_details.html', context)

def lenses_page(request):
    return render(request, 'user/lenses_page.html')

def about(request):
    return render(request, 'user/about.html')

def Profile(request):
    return render(request , 'user/Profile.html')

def adminhome(request):
    product=Product.objects.all()
    return render(request, 'adminpage/adminhome.html',{'product': product})

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




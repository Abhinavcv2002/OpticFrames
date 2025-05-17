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
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Corrected line to use create_user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('userup')  

    return render(request, "user/userup.html")

def userup(request):
    if request.method == 'POST':  
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Corrected line to use create_user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('userup')  

    return render(request, "user/userup.html")

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


def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.totalprice for item in cart_items)
    
    # Get user's saved addresses
    saved_addresses = Address.objects.filter(user=user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Check if using an existing address or creating a new one
        if 'address_id' in request.POST:
            # Using existing address
            address_id = request.POST.get('address_id')
            shipping_address = Address.objects.get(id=address_id, user=user)
            
            # Use the details from the existing address
            name = shipping_address.name
            address = shipping_address.address
            city = shipping_address.city
            state = shipping_address.state
            pincode = shipping_address.pincode
            phone = shipping_address.phone
            
        else:
            # Creating a new address
            name = request.POST.get('name')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            phone = request.POST.get('phone')
            
            # Save address if checkbox is checked
            if request.POST.get('save_for_future'):
                shipping_address = Address.objects.create(
                    user=user,
                    name=name,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    phone=phone
                )
            else:
                # Use address for this order but don't save it
                shipping_address = None
        
        # Create one order per cart item
        for item in cart_items:
            order = Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                amount=item.totalprice,
                status="Pending",
                # Store the address details
                shipping_name=name,
                shipping_address=address,
                shipping_city=city,
                shipping_state=state,
                shipping_pincode=pincode,
                shipping_phone=phone,
                # Link to the saved address if we saved one
                address=shipping_address,
                payment_method=payment_method
            )
            
            # If using online payment, update with payment details
            if payment_method == 'online':
                # Implement payment gateway integration here
                # This would typically involve redirecting to a payment page
                # and updating the order status and payment IDs upon return
                pass
        
        # Clear the cart after purchase
        cart_items.delete()
        
        # Redirect to order confirmation page
        return redirect('order_summary')
    
    return render(request, 'user/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'saved_addresses': saved_addresses
    })    
  

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
    product = Product.objects.all()
    return render(request, 'adminpage/adminhome.html', {'product': product})

def adminadd(request):
    # Get all available options for dropdown fields
    categories = category.objects.all()
    genders = Gender.objects.all()
    materials = Material.objects.all()
    frame_types = FrameType.objects.all()
    frame_shapes = FrameShape.objects.all()
    frame_styles = FrameStyle.objects.all()
    
    if request.method == 'POST':
        # Collect form data
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        color = request.POST.get('color')
        
        # Get foreign key objects
        gender_id = request.POST.get('gender')
        material_id = request.POST.get('material')
        frame_type_id = request.POST.get('frame_type')
        frame_shape_id = request.POST.get('frame_shape')
        frame_style_id = request.POST.get('frame_style')
        category_id = request.POST.get('category')
        
        # Get image files
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        
        # Validate required fields
        if not all([name, price, description, main_image]):
            messages.error(request, "Please fill in all required fields!")
            return render(request, 'adminpage/adminadd.html', {
                'categories': categories,
                'genders': genders,
                'materials': materials,
                'frame_types': frame_types,
                'frame_shapes': frame_shapes,
                'frame_styles': frame_styles,
            })

        try:
            # Create product with all details
            product = Product(
                name=name,
                price=float(price),
                description=description,
                color=color,
                image=main_image,  # Set main image
            )
            
            # Set foreign keys if provided
            if gender_id:
                try:
                    gender_obj = Gender.objects.get(id=gender_id)
                    product.gender = gender_obj
                except Gender.DoesNotExist:
                    pass
                
            if material_id:
                try:
                    material_obj = Material.objects.get(id=material_id)
                    product.material = material_obj
                except Material.DoesNotExist:
                    pass
                
            if frame_type_id:
                try:
                    frame_type_obj = FrameType.objects.get(id=frame_type_id)
                    product.frameType = frame_type_obj
                except FrameType.DoesNotExist:
                    pass
                
            if frame_shape_id:
                try:
                    frame_shape_obj = FrameShape.objects.get(id=frame_shape_id)
                    product.frameShape = frame_shape_obj
                except FrameShape.DoesNotExist:
                    pass
                
            if frame_style_id:
                try:
                    frame_style_obj = FrameStyle.objects.get(id=frame_style_id)
                    product.frameStyle = frame_style_obj
                except FrameStyle.DoesNotExist:
                    pass
                
            if category_id:
                try:
                    category_obj = category.objects.get(id=category_id)
                    product.category = category_obj
                except category.DoesNotExist:
                    pass
            
            # Save the product
            product.save()
            
            # Handle additional images (up to 5)
            if additional_images:
                for i, img in enumerate(additional_images[:5]):
                    if i == 0:
                        product.image1 = img
                    elif i == 1:
                        product.image2 = img
                    elif i == 2:
                        product.image3 = img
                    elif i == 3:
                        product.image4 = img
                    elif i == 4:
                        product.image5 = img
                
                # Save again with additional images
                product.save()
            
            messages.success(request, f"Product '{name}' added successfully!")
            return redirect('adminhome')
        
        except Exception as e:
            messages.error(request, f"Error adding product: {str(e)}")
    
    # For GET requests or when form submission fails
    return render(request, 'adminpage/adminadd.html', {
        'categories': categories,
        'genders': genders,
        'materials': materials,
        'frame_types': frame_types,
        'frame_shapes': frame_shapes,
        'frame_styles': frame_styles,
    })

def admin_logout_view(request):
    logout(request)
    return render(request, 'adminpage/adminin.html')




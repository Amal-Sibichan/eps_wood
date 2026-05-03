from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate
from django.db.models import Q  
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
# Create your views here.

# def adm(request):
#     adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='admin',password='1234',usertype='admin')
#     adm.save()
#     return redirect('/')

def index(request):
    if request.session.get('usertype') == 'admin':
        return redirect('admin_dashboard')
    elif request.session.get('usertype') == 'owner':
        return redirect('owner_dashboard')
    elif request.session.get('usertype') == 'customer':
        return redirect('customer_dashboard')
    return render(request, 'index.html')


def admin_dashboard(request):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    pending_owners_count = Owner.objects.filter(status='pending').count()
    return render(request, 'admin/admin_dashboard.html',{'pending_owners_count':pending_owners_count})

def owner_dashboard(request):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    login = Login.objects.get(id=request.session.get('uid'))
    owner = Owner.objects.get(login=login)
    return render(request, 'owner/owner_dashboard.html', {'login': login, 'owner': owner})

def customer_dashboard(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    return render(request, 'customer/customer_dashboard.html')


def customer_register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        mobile = request.POST['mobile']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES.get('profile_image')

        # Email validation
        if not (email.endswith('@gmail.com') or email.endswith('.in')):
            messages.info(request, 'Email must be valid (@gmail.com or .in)')
            return redirect('customer_register')

        # Mobile validation
        if not (mobile.isdigit() and len(mobile) == 10):
            messages.info(request, 'Mobile number must be 10 digits')
            return redirect('customer_register')

        # Username exists
        if Login.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('customer_register')

        login = Login.objects.create_user(
            username=username,
            password=password,
            usertype='customer',
            viewpassword=password
        )

        Customer.objects.create(
            login=login,
            full_name=full_name,
            address=address,
            mobile=mobile,
            email=email,
            profile_image=image
        )

        messages.success(request, 'Customer registered successfully')
        return redirect('customer_register')

    return render(request, 'customer_register.html')



def owner_register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        mobile = request.POST['mobile']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        owner_type = request.POST['type']
        image = request.FILES.get('profile_image')

        # Email validation
        if not (email.endswith('@gmail.com') or email.endswith('.in')):
            messages.info(request, 'Email must be valid (@gmail.com or .in)')
            return redirect('owner_register')

        # Mobile validation
        if not (mobile.isdigit() and len(mobile) == 10):
            messages.info(request, 'Mobile number must be 10 digits')
            return redirect('owner_register')

        # Username exists
        if Login.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('owner_register')

        login = Login.objects.create_user(
            username=username,
            password=password,
            usertype='owner',
            viewpassword=password,
            is_active=False
        )

        Owner.objects.create(
            login=login,
            full_name=full_name,
            address=address,
            mobile=mobile,
            email=email,
            profile_image=image,
            type=owner_type
        )

        messages.success(request, 'Owner registered successfully')
        return redirect('owner_register')

    return render(request, 'owner_register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check for admin (hardcoded)
        if username == 'admin' and password == '1234':
            request.session['uid'] = 0  # no user id for admin
            request.session['usertype'] = 'admin'
            messages.success(request, "Login successful as Admin")
            return redirect('/admin_dashboard/')
        
        # Check user in Login model
        user = authenticate(username=username, password=password)
       
        if user:
            request.session['uid'] = user.id
            request.session['usertype'] = user.usertype

            if user.usertype == 'customer':
                customer = Customer.objects.get(login=user)
                if customer.status == 'block':
                    messages.error(request, "Your account is blocked by admin contact admin")
                    return redirect('login')
                messages.success(request, "Login successful as Customer")
                return redirect('/customer_dashboard/')

            elif user.usertype == 'owner':
                owner = Owner.objects.get(login=user)
                if owner.status == 'pending' or owner.status == 'revoked':
                    messages.error(request, "Your account is not activated by admin contact admin")
                    return redirect('login')
                messages.success(request, "Login successful as Owner")
                return redirect('/owner_dashboard/')

            else:
                messages.error(request, "Invalid user type")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# Profile of owner

def owner_profile(request):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner = Owner.objects.get(login_id=request.session['uid'])
    return render(request, 'owner/owner_profile.html', {'owner': owner})

#update owner profile


def owner_update_profile(request):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner=Owner.objects.get(login_id=request.session['uid'])
    login=Login.objects.get(id=request.session['uid'])
    if request.method == 'POST':
        name=request.POST['full_name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        address=request.POST['address']
        image=request.FILES.get('profile_image')
        owner.login=login
        owner.full_name=name
        owner.mobile=mobile
        owner.email=email
        owner.address=address
        if image:
            owner.profile_image=image
        owner.save()
        messages.success(request,'Profile updated successfully')
        return redirect('owner_profile')
    return render(request,'owner/owner_update_profile.html',{'owner':owner,'login':login})
    
def add_products(request):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner=Owner.objects.get(login_id=request.session['uid'])
    login=Login.objects.get(id=request.session['uid'])
    errors={}
    if request.method == 'POST':
        product_name=request.POST['product_name']
        category=request.POST['category']
        price=request.POST['price']
        unit=request.POST['unit']
        stock_quantity=request.POST['stock_quantity']
        wood_type = request.POST.get('wood_type')
        thickness = request.POST.get('thickness')
        if not thickness:
            thickness = None
            
        size = request.POST.get('size')
        grade = request.POST.get('grade')
        description = request.POST.get('description')
        
        delivery_available = 'delivery_available' in request.POST
        
        delivery_charge = request.POST.get('delivery_charge')
        if not delivery_charge:
            delivery_charge = None
        product_images=request.FILES.getlist('product_images')
        if float(price)<1:
            errors['price']='Price must be greater than 0'
        if int(stock_quantity)<1:
            errors['stock_quantity']='Stock quantity must be greater than 0'
        if delivery_charge and float(delivery_charge)<1:
            errors['delivery_charge']='Delivery charge must be greater than 0'
        

        if errors:
            return render(request,'owner/add_products.html',{'owner':owner,'login':login,'errors':errors})
        product=Product.objects.create(
            owner=owner,
            product_name=product_name,
            category=category,
            price=price,
            unit=unit,
            stock_quantity=stock_quantity,
            wood_type=wood_type,
            thickness=thickness,
            size=size,
            grade=grade,
            description=description,
            delivery_available=delivery_available,
            delivery_charge=delivery_charge,
        )

        for image in product_images:
            ProductImage.objects.create(
                product=product,
                image=image
            )
        

        messages.success(request,'Product added successfully')
        return redirect('add_products')

    return render(request,'owner/add_products.html',{'owner':owner,'login':login})

def product_list(request):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner=Owner.objects.get(login_id=request.session['uid'])
    login=Login.objects.get(id=request.session['uid'])
    
    # 2. Start with the base queryset
    products = Product.objects.filter(owner=owner).prefetch_related('images')

    # 3. Capture GET parameters from search/filter boxes
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')

    # 4. Apply Filters if they exist
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | 
            Q(wood_type__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_filter:
        products = products.filter(category=category_filter)

    if stock_filter:
        products = products.filter(availability_status=stock_filter)

    # 5. Final sorting (Newest first)
    products = products.order_by('-created_at')

    context = {
        'products': products,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter
    }
    return render(request, 'owner/product_list.html', context)


def edit_product(request, product_id):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner=Owner.objects.get(login_id=request.session['uid'])
    product = get_object_or_404(Product, id=product_id, owner=owner)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.category = request.POST.get('category')
        product.description = request.POST.get('description')
        product.wood_type = request.POST.get('wood_type')
        product.thickness = request.POST.get('thickness') or None
        product.size = request.POST.get('size')
        product.grade = request.POST.get('grade')
        product.price = request.POST.get('price')
        product.unit = request.POST.get('unit')
        product.stock_quantity = request.POST.get('stock_quantity')
        
        if int(product.stock_quantity) > 0:
            product.availability_status = 'in_stock'
        else:
            product.availability_status = 'out_of_stock'

        product.save()

        # Handle New Images (if any)
        new_images = request.FILES.getlist('product_images')
        for img in new_images:
            ProductImage.objects.create(
                product=product,
                image=img,
                is_primary=False  # Keep the old primary image
            )

        return redirect('product_list')

    return render(request, 'owner/edit_product.html', {'product': product})

def delete_product(request, product_id):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')


def customer_profile(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer=Customer.objects.get(login_id=request.session['uid'])

    return render(request,'customer/customer_profile.html',{'customer':customer})

def customer_profile_update(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer=Customer.objects.get(login_id=request.session['uid'])
    login=Login.objects.get(id=request.session['uid'])
    errors={}    
    if request.method == 'POST':
        full_name=request.POST['full_name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        address=request.POST['address']
        image=request.FILES.get('profile_image')
        customer.full_name=full_name
        customer.mobile=mobile
        customer.email=email
        customer.address=address
        if image:
            customer.profile_image=image
        customer.save()
        messages.success(request,'Profile updated successfully')
        return redirect('customer_profile')
    return render(request,'customer/customer_profile_update.html',{'customer':customer,'login':login})

def products(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    product_list = Product.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')

    # 2. Capture GET parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # 3. Apply Filters
    if search_query:
        product_list = product_list.filter(
            Q(product_name__icontains=search_query) | 
            Q(wood_type__icontains=search_query)
        )
    
    if category_filter:
        product_list = product_list.filter(category=category_filter)

    # 4. Pagination (Show 6 products per page)
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request,'customer/products.html',context)

def product_details(request,p_id):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    product = get_object_or_404(Product, id=p_id, is_active=True)
    return render(request,'customer/product_details.html',{'product':product})

def my_cart(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer=Customer.objects.get(login_id=request.session['uid'])
    cart, created = Cart.objects.get_or_create(user=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'customer/my_cart.html', context)

def add_to_cart(request, product_id):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer=Customer.objects.get(login_id=request.session['uid'])
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity=request.POST.get('quantity')
        cart, created = Cart.objects.get_or_create(user=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        messages.success(request,'Added to cart')
    return redirect('my_cart')


def remove_item(request,item_id):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    item=CartItem.objects.get(id=item_id)
    item.delete()
    messages.success(request,'Item removed from cart')
    return redirect('my_cart')


def checkout(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer=Customer.objects.get(login_id=request.session['uid'])
    cart = get_object_or_404(Cart, user=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    if  not cart_items.exists():
        return redirect('my_cart')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request,'customer/check_out.html',{'cart_items':cart_items,'total_price':total_price})

def place_order(request):   
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer = Customer.objects.get(login_id=request.session['uid'])
    cart = get_object_or_404(Cart, user=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('my_cart')

    if request.method == 'POST':
        
        payment_method = request.POST.get('payment_method')
        total_price = sum(item.product.price * item.quantity for item in cart_items)

       
        order = Order.objects.create(
            user=customer,
            total_price=total_price,
            payment_method=payment_method,  
            status='Pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            product = item.product
            product.stock_quantity -= item.quantity
            
            if product.stock_quantity <= 0:
                product.availability_status = 'out_of_stock'
            
            product.save()
        cart_items.delete()

        messages.success(request, f"Order placed successfully using {payment_method.upper()}!")
        return redirect('order_history') 

    return redirect('my_cart')

def order_history(request):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer = Customer.objects.get(login_id=request.session['uid'])

    # Fetch order items instead of orders
    order_items = OrderItem.objects.filter(order__user=customer).select_related('order','product','product__owner').order_by('-order__created_at')

    return render(request,'customer/order_history.html',{'order_items': order_items})

def customer_order_details(request, item_id):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer = Customer.objects.get(login_id=request.session['uid'])
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=customer)
    context = {
        'item': order_item,
        'order': order_item.order,
        'customer': customer,
    }
    return render(request, 'customer/customer_order_details.html', context)

def cancel_order(request, item_id):
    if request.session.get('usertype') != 'customer':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_item.status = 'Cancelled'
    order_item.save()
    product = order_item.product
    product.stock_quantity += order_item.quantity
    product.save()
    messages.success(request, "Order item cancelled successfully")
    return redirect('order_history')


# order requests 

def incoming_orders(request):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner=Owner.objects.get(login_id=request.session['uid'])
    my_order_items = OrderItem.objects.filter(
        product__owner=owner

    ).select_related('order', 'order__user', 'product').order_by('-order__created_at')
    return render(request, 'owner/incoming_orders.html', {'order_items': my_order_items})

def update_order_status(request, item_id):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    if request.method == 'POST':
        order_item = get_object_or_404(OrderItem, id=item_id)
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Delivered']:
            order_item.status = new_status
            order_item.save()
            
        messages.success(request, f"Order status updated to {new_status}")
    return redirect('incoming_orders')

def order_details(request, item_id):
    if request.session.get('usertype') != 'owner':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner=Owner.objects.get(login_id=request.session['uid'])
    order_item = get_object_or_404(OrderItem, id=item_id,product__owner=owner)
    context = {
        'item': order_item,
        'order': order_item.order,
        'customer': order_item.order.user,
    }
    return render(request, 'owner/order_details.html', context)


# admin views

def pending_owners(request):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    pending_owners = Owner.objects.filter(status='pending')
    pending_owners_count = pending_owners.count()
    return render(request, 'admin/pending_owners.html', {'pending_owners': pending_owners,'pending_owners_count':pending_owners_count})

def approve_owner(request, owner_id):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner = Owner.objects.get(id=owner_id)
    owner.status='approved'
    owner.login.is_active = True
    owner.login.save()
    owner.save()
    return redirect('pending_owners')

def reject_owner(request, owner_id):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owner = Owner.objects.get(id=owner_id)
    owner.status='revoked'
    owner.save()
    return redirect('pending_owners')

def owner_list(request):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    owners = Owner.objects.all()
    return render(request, 'admin/owner_list.html', {'owners': owners})


def customer_list(request):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customers = Customer.objects.all()
    return render(request, 'admin/customer_list.html', {'customers': customers})

def toggle_customer_status(request, customer_id, action):
    if request.session.get('usertype') != 'admin':
        messages.error(request, "You are not authorized to access this page")
        return redirect('login')
    customer = Customer.objects.get(id=customer_id)
    if action == 'block':
        customer.status = 'block'
    elif action == 'unblock':
        customer.status = 'unblock'
    customer.save()
    return redirect('customer_list')


def logout(request):
    request.session.flush()
    return redirect('login')
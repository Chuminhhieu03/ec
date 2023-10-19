from datetime import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Product, ImageGallery, Cart, Order, OrderDetail
from django.http import JsonResponse
# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = [product.category.lower() for product in products if product.category]
    set_categories = set(categories)
    return render(request, "index.html", {'products': products, 'categories': set_categories})

def testimo(request):
    return render(request,"testimonials.html")

def contact(request):
    return render(request,'contact.html')

def portfolio(request):
    if request.method == "GET":
        products = Product.objects.all()
        categories = [product.category.lower() for product in products if product.category]
        set_categories = set(categories)
        return render(request, "portfolio.html", {'products': products, 'categories': set_categories})
    if request.method == "POST":
        try:  
            product_name = request.POST.get('product_name')
            products = Product.objects.all()
            if product_name:
                products = products.filter(product_name__icontains=product_name)
            categories = [product.category.lower() for product in products if product.category]
            set_categories = set(categories)
            # Chuyển đổi QuerySet thành danh sách Python
            products_list = list(products.values())
            return JsonResponse({'status': 'success', 'products': products_list, 'categories': list(set_categories)})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Cant Search'})

    
def detail(request,id):
    product = get_object_or_404(Product,id=id)
    photos = ImageGallery.objects.filter(product = product)
    return render(request,"portfolio-details.html",{
        'product' : product,
        'photos' : photos
    })

def showCart(request):
    if not request.user.is_authenticated:
        messages.warning(request,"You need to log in to access")
        return redirect('/auth/login')
    carts = Cart.objects.filter(user=request.user)
    total_cost = sum(cart.total_cost for cart in carts)
    total_costAll = total_cost + 10
    return render(request, 'payment.html', {'carts': carts, 'total_cost': total_cost, 'total_costAll' : total_costAll})

def addToCart(request):
    if not request.user.is_authenticated:
        messages.warning(request,"You need to log in to access")
        return redirect('/auth/login')
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    quantity = request.GET.get('quantity')

    if Cart.objects.filter(user=user, product=product).exists():
        messages.warning(request, 'You already have this product in your cart.')
    else:
        Cart(user=user, product=product, quantity=quantity).save()
        messages.success(request, 'You have successfully added the product to your cart.')

    return redirect('/show')


def increaseCart(request):
    if request.method == 'POST':
        cartId = request.POST.get('cartid')
        print(cartId)
        try:
            cart = Cart.objects.get(id=cartId)
            cart.quantity += 1
            cart.save()
            return JsonResponse({'status': 'success', 'new_quantity': cart.quantity})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def decreaseCart(request):
    if request.method == 'POST':
        cartId = request.POST.get('cartid')
        try:
            cart = Cart.objects.get(id=cartId)
            if(cart.quantity == 1):
                cart.quantity = 1
            else:
                cart.quantity -= 1
            cart.save()
            return JsonResponse({'status': 'success', 'new_quantity': cart.quantity})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def removeCart(request):
    if request.method == 'POST':
        cartId = request.POST.get('cartid')
        try:
            item_to_delete = Cart.objects.get(id=cartId)
            item_to_delete.delete()
            return JsonResponse({'status': 'success', 'message': 'Item deleted successfully'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


def createOrder(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        value = request.POST.get('value')
        user = request.user
        date = datetime.now().strftime('%Y-%m-%d')
        try:
            # lưu thông tin order
            new_order = Order(user=user, name=name, phone=phone, address=address, value=value, status="Received", date=date)
            new_order.save()
            carts = Cart.objects.filter(user=user)

            # Tạo order detail
            for cart in carts:
                order_detail = OrderDetail(
                    order=new_order,
                    product=cart.product,
                    quantity=cart.quantity
                )
                order_detail.save()
                cart.delete()
                #Xóa đi cart tương ứng
            messages.success(request,"You have create order success")
            return redirect('/order')
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Order cant create'})

def getOrder(request):
    if not request.user.is_authenticated:
        messages.warning(request,"You need to log in to access")
        return redirect('/auth/login')
    orders = Order.objects.filter(user=request.user)
    return render(request,'order.html',{'orders' : orders })

def getOrderdt(request,id):
    if not request.user.is_authenticated:
        messages.warning(request,"You need to log in to access")
        return redirect('/auth/login')
    try:
        order = Order.objects.get(id_order=id)
        orderDetails = OrderDetail.objects.filter(order=order)
        return render(request,'order-detail.html', {'order' : order,'orderDatails' : orderDetails})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'status': 'error', 'message': 'Order detail error'})

def demo(request):
    return render(request,'demo.html')
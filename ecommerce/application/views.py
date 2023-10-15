from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Product, ImageGallery, Cart
from django.http import JsonResponse
# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = [product.category.lower() for product in products if product.category]
    set_categories = set(categories)
    return render(request, "index.html", {'products': products, 'categories': set_categories})


def detail(request,id):
    product = get_object_or_404(Product,id=id)
    photos = ImageGallery.objects.filter(product = product)
    return render(request,"portfolio-details.html",{
        'product' : product,
        'photos' : photos
    })

def showCart(request):
    carts = Cart.objects.filter(user=request.user)
    total_cost = sum(cart.total_cost for cart in carts)
    return render(request, 'payment.html', {'carts': carts, 'total_cost': total_cost})

def addToCart(request):
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

def testimo(request):
    return render(request,"testimonials.html")

def contact(request):
    return render(request,'contact.html')

def portfolio(request):
    products = Product.objects.all()
    categories = [product.category.lower() for product in products if product.category]
    set_categories = set(categories)
    return render(request, "portfolio.html", {'products': products, 'categories': set_categories})
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse


from django.contrib.auth.decorators import login_required
from store.models import Cart
# from store.models import Coupon
from store.models import Order
from store.models import OrderItem
from store.models import Product,Profile
from django.contrib.auth.models import User


import random

@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity :
            # Cart.objects.delete(id=item.id)
            item.delete()

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()

    context = {'cartitems':cartitems, 'total_price' : total_price, 'userprofile':userprofile}
    return render(request, "store/checkout.html", context)

@login_required(login_url='loginpage')
def placeorder(request):

    if request.method == 'POST':
        
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name :
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

            

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'gokul'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'gokul'+str(random.randint(1111111,9999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            # To decrease the product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        #To clear user's Cart
        Cart.objects.filter(user=request.user).delete()


        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed successfully"})
        else:
            messages.success(request, "Your order has been placed successfully")
    return redirect('/')


@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.selling_price * item.product_qty

    return JsonResponse({

        'total_price': total_price
    })

def orders(request):
    return HttpResponse("My orders page")








# for coupons


# @login_required(login_url='loginpage')
# def ApplyCoupon(request):
#     print("hai im here")
#     if request.method == 'POST':
#         coupons = Coupon.objects.all()
#         context= {'coupons': coupons}
#         return render(request, "store/checkout.html",context)
        
    
        # grand_total=request.POST.get('key2')
        # grand_totals=float(grand_total)
        # try:
        #     coupons = Coupon.objects.get(code=coupon_code)
            
        # except:
        #     print("its working on except")
        # discount_amount=coupons.discount
        # total=grand_totals-discount_amount
        # request.session['grand_total'] = total
        # return JsonResponse({"total": f"{total}", "discount_amount": f"{discount_amount}"})

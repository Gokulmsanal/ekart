from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from store.models import Wishlist

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request,'store/wishlist.html', context)
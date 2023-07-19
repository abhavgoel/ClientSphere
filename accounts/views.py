from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


# Create your views here.

@unauthorized_user
def registerPage(request):
   
    form = CreateUserForm()
    if request.method=='POST':
        form =CreateUserForm(request.POST)
        if  form.is_valid():
            user = form.save()
            username=form.cleaned_data.get('username')
            group =Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            messages.success(request,"Account was created for " + username)
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

@unauthorized_user
def loginPage(request):
   
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')

    context={} 
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') 
@admin_only
def home(request):
    customers=Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customers,'orders':orders,'total_customers':total_customers,'total_orders':total_orders,
               'delivered':delivered,'pending':pending}

    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def products(request):
   products = Product.objects.all()
   return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customers = Customer.objects.get(id=pk_test)

    orders = Order.objects.filter(customer = pk_test)
    orders_count = orders.count()

    filter = OrderFilter(request.GET,queryset=orders)#query set = intial data
    orders = filter.qs # here filter applied to data
    # print(request) 
    context={'customers':customers,'orders':orders,'orders_count':orders_count,"filter":filter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)
    if request.method=='POST':
        form = OrderForm(request.POST, instance = order )
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    item = Order.objects.get(id=pk)
    if request.method =='POST':
        item.delete()
        return redirect('/')
    context={'item':item}
    return render(request,'accounts/delete.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    # print('orders--->',orders)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context={'orders':orders,'total_orders':total_orders,
               'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['customer'])
def accounSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance = customer)
    if request.method=='POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'accounts/account_settings.html',context)


'''
file structure to import templates

-accounts
---templates
------accounts
---------dashboard.html

'''
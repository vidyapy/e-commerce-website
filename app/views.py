from django.utils import timezone
from django.shortcuts import render,redirect
from .forms import ProductForm
from app.models import  *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})

def add_product(request):
    form=ProductForm()
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print("not working")
            messages.info(request,"not working")

    context = {
        'form':form
    }
    return render(request,'core/add_product.html',context)


def product_desc(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html',{'product':product})


def add_cart(request,pk):
    #get that product with id
    product=Product.objects.get(pk=pk)
    #order item:
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user = request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"Added quantity Item")
            return redirect('product_desc',pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"item added to the cart")
            return redirect ('product_desc',pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        
        messages.info(request,"Item is  added to the cart")
        return redirect('product_desc',pk=pk)




def orderlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists:
        order= Order.objects.get(user=request.user,ordered=False)
        return render(request,'core/orderlist.html',{'order':order})
    return render(request,'core/orderlist.html',{'message':"empty cart"})

def add_item(request,pk):
    #get that product with id
    product=Product.objects.get(pk=pk)
    #order item:
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user = request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,"Added quantity Item")
                return redirect('orderlist')

            else:
                messages.info(request,"product is out of stock")
                return redirect('orderlist')
        else:
            order.items.add(order_item)
            messages.info(request,"item added to the cart")
            return redirect ('product_desc',pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        
        messages.info(request,"Item is  added to the cart")
        return redirect('product_desc',pk=pk)
    



def remove_item(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item=OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False,

            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order_item.delete()
            messages.info(request,"quantity is updated")
            return redirect('orderlist')
        
        else:
            messages.info(request,'This item is not in your cart')
            return redirect('orderlist')

    else:
        messages.info(request,"no order list")
        return redirect('orderlist')




# def checkout_page(request):
#     if CheckoutAddress.objects.filter(user=request.user).exists():
#         return render(request,'checkout.html',{'payment_allow':'allow'})
#     if request.method == 'POST':
#         form= CheckoutForm(request.POST)
#         try:
#             if form.is_valid():
#                 street_address=form.changed_data.get('street_address')
#                 appartment_address=form.changed_data.get('appartment_address')
#                 country=form.changed_data.get('country')
#                 zip=form.changed_data.get('zip')

#                 checkout_address = CheckoutAddress(
#                     user=request.user,
#                     street_address=street_address,
#                     appartment_address=appartment_address,
#                     country=country,
#                     zip=zip

#                 )
#                 checkout_address.save()
#                 print("it should render the summary  page")
#                 return render(request,'checkout.html',{'payment_allow':'allow'})
#         except ObjectDoesNotExist:
#             messages.warning(request,"Failed checkout")
#             return redirect('checkout')
#     else:
#         form=CheckoutForm()
#         return render(request,'checkout.html',{'form':form})




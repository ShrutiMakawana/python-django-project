from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
#from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from app1.models import Contact,Appointment,Employee,Service,Gallery,Product,Profile,Cart,Address,Order,OrderItem
from app1.forms import AppointmentForm,AddressForm
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import uuid
from django.urls import reverse
import razorpay
from django.views import View
from django.db.models import Q , F
from django.http import JsonResponse
from django.db.models import Count



# Create your views here.
def index1(request):
    empobj = Employee.objects.all()
    service_obj = Service.objects.all()
    gallery_obj = Gallery.objects.all()
    context = {
        'employee' : empobj,
        'service' : service_obj,
        'gallery' : gallery_obj,    
    }
    return render(request,"index1.html",context)

def generate_otp():
    return str(random.randint(111111,999999))

def signup(request):
    # user = User.objects.all()
    # context = {
    #     'user' : user
    # }
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        #pass2 = request.POST.get('password2')
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists !!')
            return render(request, 'signup.html')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request,'E-mail already exists !!')
                return render(request, 'signup.html')
            else:
                otp = generate_otp()
                subject = "OTP Verification"
                message = f'''Dear {uname}, \n\n\t Your otp is {otp} \n\n Best regards,\n SmartLook.'''
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]

                send_mail(subject,message,email_from,recipient_list,fail_silently=False)

                request.session['otp'] = otp
                request.session['new_user_data'] = {
                    'username': uname,
                    'email': email,
                    'password': pass1
                }
                
                messages.success(request, 'An otp has been sent to your email for verification!!')

                return redirect('verify_otp')
    return render(request,"signup.html")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp'):
            user_data = request.session.get('new_user_data')
            if user_data:
                user = User.objects.create_user(user_data['username'],user_data['email'], user_data['password'])
                del request.session['otp']
                del request.session['new_user_data']
                messages.success(request, 'You have signed up successfully!')
                pobj = Profile.objects.create(user = user)
                pobj.save()
                return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect("verify_otp")
    return render(request, "otp.html")

def change_password(request,token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(token = token).first()
        context = {'user_id':profile_obj.user.id}

        #print(profile_obj)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request,'No User found')
                return redirect('change_password/{token}')
            
            if new_password != confirm_password:
                messages.success(request,'Both passwords that you entered must be equal..!!')
                return redirect(reverse('change_password/{token}'))
            else:
                user_obj = User.objects.get(id = user_id)
                user_obj.set_password(new_password)
                user_obj.save()
                return redirect('login')


    except Exception as e:
        print(e)

    return render(request,"change_password.html",context)

def send_forget_password_mail(email,token):
    
    subject = "Your forget password link"
    msg = f'Hi, click on the link to reset your password http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject,msg,email_from,recipient_list)
    return True


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).first():
            messages.success(request,'No User found with this email..!!')
            return redirect('forgot_password')
        
        user_obj = User.objects.get(email=email)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user=user_obj)
        profile_obj.token = token
        profile_obj.save()
        send_forget_password_mail(email,token)
        messages.success(request,'An email is sent')
        return redirect('forgot_password')

    return render(request,"forgot.html")

def userpro(request):
    user = User.objects.all()
    appointment = Appointment.objects.all()
    order = Order.objects.filter(user=request.user)
    context = {
        'user' : user,
        'appointment' : appointment ,
        'order':order,
    }
    return render(request,"user.html",context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            messages.error(request,"Incorrect Username or Password !!!")
            return render(request,'login.html')
    return render(request,"login.html")

def saveEnquiry(request):
    #import pdb;pdb.set_trace();
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_obj = Contact.objects.create(name=name,email=email,subject=subject,message=message,date=datetime.today())
        contact_obj.save()
        subject = f'Thank you for contacting us,{contact_obj.name} !'
        message = f'''Hello {contact_obj.name}, \n\n\t Thank you for getting in touch with us. We appreciate your interest in our services/products. We have received your inquiry regarding {contact_obj.subject}, and our team is currently reviewing it. We would try to respond as soon as possible. Thank you once again for reaching out.
        \n\nBest regards, \nSmartLook\nsmartlooksalon27@gmail.com'''
        email_from = settings.EMAIL_HOST_USER
        #recipient_list = [Appointment.email]
        recipient_list = [contact_obj.email,]
        send_mail( subject, message, email_from, recipient_list,fail_silently=False )

        return redirect('index')
    return render(request,'index')

# def product_detail(request):
#     product_obj = Product.objects.all()

#     return render(request,'product_detail.html',{'product':product_obj})

# def cart(request):
#     # if request.user.is_anonymous:
#     #     return redirect("login")
#     product_obj = Product.objects.all()
#     context = {
#         "product" : product_obj
#     }
    
#     return render(request,"product.html",context)

def log_out(request):
    logout(request)
    return redirect("login")

#@login_required
def appointmentbooking(request):
    if request.user.is_anonymous:
        return redirect("login")
    else:
    #import pdb;pdb.set_trace();
        slot_available = True
        if request.method == "POST":
            form = AppointmentForm(request.POST)
            if form.is_valid():
                # user_id = User.id
                # user = User.objects.get(pk=user_id)
                # user = User.objects.get(pk=id)
                user = request.user
                name = request.POST.get('name')
                age = request.POST.get('age')
                mobileno = request.POST.get('mobileno')
                email = request.POST.get('email')
                service = request.POST.get('service')
                category = request.POST.get('category')
                appointment_date = request.POST.get('date')
                slot = request.POST.get('slot')
                #en = Appointment(name=name,email=email,subject=subject,message=message,date=datetime.today())
                #en.save()
                #appointment_datetime = datetime.strptime(appointment_date, '%d-%m-%Y')
                existing_appointments = Appointment.objects.filter(service=service,slot=slot,date=appointment_date)
                    # If appointments already exist for the service and slot, display an error message
                if existing_appointments.exists():
                    slot_available = False
                    if slot_available == False:
                        
                        messages.success(request, '''\nSorry, Already Booked!!  Please select another slot for your service.''')
                        return redirect('index')
                else:
                    appobj = Appointment(
                                        user=user,
                                        name = name,
                                        age = age,
                                        mobileno = mobileno,
                                        email = email,
                                        service = service,
                                        category = category,
                                        date = appointment_date,
                                        slot = slot )
                    appointment = form.save(commit=False)

                    # Save the user who made the appointment if they're logged in
                    if request.user.is_authenticated:
                        appointment.user = request.user
                    # Save the appointment to the database
                        appointment.save()
                        
                        subject = 'Appointment Booked'
                        message = f'''Hello {appointment.name}, \nYour appointment for {appointment.service} is booked on {appointment.date} between {appointment.slot} . \nThank you for visiting SmartLook.'''
                        email_from = settings.EMAIL_HOST_USER
                        #recipient_list = [Appointment.email]
                        recipient_list = [appobj.email,]
                        send_mail( subject, message, email_from, recipient_list,fail_silently=False )
                        messages.success(request,"Your appointment is booked.\n Check your mail for confirmation..!!")
                        return redirect("index")
                    return render(request,"index1.html")
                

def cancel_appointment(request,id):
    appointment = Appointment.objects.get(pk=id)
    if appointment.user == request.user.username:
        appointment.delete()
        messages.success(request,"Your appointment is successfully deleted..!!")
        return redirect('userpro')
    return redirect('userpro')






def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        product_id=request.GET.get('prod_id')
        product=Product.objects.get(pro_id=product_id)
        Cart(user=user,product=product).save()
        return redirect("/cart")
    else:
        messages.warning(request,"Please login to purchase the products !!")
        return redirect('login')

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())


class checkout(View):
    def get(self,request):
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        famount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            famount = famount+value
        totalamount = famount + 40

        return render(request,'checkout.html',locals())


def address(request):
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            mobileno = request.POST.get('mobileno')
            payment_method = request.POST.get('payment_method')
            address_obj = Address(                  user=user,
                                                    address=address,
                                                    city=city,
                                                    state=state,
                                                    pincode=pincode,
                                                    mobileno=mobileno,
                                                    payment_method=payment_method
                                            )
            address_obj.save()
        
    return redirect('order')

def order(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    address = Address.objects.filter(user=user).latest('id')
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"order.html",locals())



class CategoryView(View):
    def get(self,request,value):
        if request.user.is_authenticated:
            product = Product.objects.filter(category=value)
            title = Product.objects.filter(category=value).values('name').annotate(total=Count('name'))
            totalitem = len(Cart.objects.filter(user=request.user))
            return render(request,"product.html",locals())
        else:
            product = Product.objects.filter(category=value)
            title = Product.objects.filter(category=value).values('name').annotate(total=Count('name'))
            return render(request,"product.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        if request.user.is_authenticated:
            product = Product.objects.filter(name=val)
            title=Product.objects.filter(category=product[0].category).values('name')
            totalitem = len(Cart.objects.filter(user=request.user))
            return render(request,"product.html",locals())
        else:
            product = Product.objects.filter(name=val)
            title=Product.objects.filter(category=product[0].category).values('name')
            return render(request,"product.html",locals())

    
class ProductDetail(View):
    def get(self,request,pk):
        if request.user.is_authenticated:

            product = Product.objects.get(pk=pk)
            cart = Cart.objects.filter(user=request.user)
            totalitem = len(Cart.objects.filter(user=request.user))
            return render(request,"product_detail.html",locals())
        else:
            product = Product.objects.get(pk=pk)
            # cart = Cart.objects.filter(user=request.user)
            # totalitem = len(Cart.objects.filter(user=request.user))
            return render(request,"product_detail.html",locals())


# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id=request.GET['prod_id']
#         print(prod_id)
#         c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))

#         # c.quantity += 1
#         # c.save()
#         user=request.user
#         cart=Cart.objects.filter(user=user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount+value
#         totalamount = amount + 40
#         data = { 
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount,
#           }
#         return JsonResponse(data)

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        # Get the product's current stock
        product = Product.objects.get(pro_id=prod_id)
        current_stock = product.stock

        # Check if adding one more quantity exceeds the available stock
        if c.quantity < current_stock:
            c.quantity += 1
            c.save()
        
            # If adding one more quantity exceeds the available stock, return an error response
            # return JsonResponse({'error': 'Maximum stock reached'})

        # Recalculate cart amount and total amount
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        total_amount = amount + 40

        data = { 
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount,
        }
        return JsonResponse(data)   

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
        totalamount = amount + 40
        # print(prod_id)
        data={ 
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
          }
        if c.quantity == 0 :
            c.delete()
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
        totalamount = amount + 40
        data={ 
            'amount':amount,
            'totalamount':totalamount,
          }
        return JsonResponse(data)
    

# def placeorder(request):
#     if request.method == 'GET':
       
#        cart = Cart.objects.all()
#        amount=0
#        for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount+value
#        totalamount = amount + 40
#        user = request.user
#        product = Cart.product
#        address = Address.address
#        quantity = Cart.quantity
#        total = totalamount

#        order_obj = OrderPlaced( user = user,product = product,address = address,quantity = quantity,total = total)
#        order_obj.save()
#     return redirect('index1')


from django.db import transaction
# def placeorder(request):
#     if request.method == 'GET':
#         user = request.user
#         cart_items = Cart.objects.filter(user=user)
#         if not cart_items.exists():
#             messages.error(request, "Your cart is empty.")
#             return redirect('/cart')

#         with transaction.atomic():  # Start of transaction
#             for item in cart_items:
#                 if item.quantity > item.product.stock:
#                     messages.error(request, f"Sorry, {item.product.name} is out of stock.")
#                     return redirect('/cart')
                
#                 # Create the order
#                 order = Order(
#                     user=user,
#                     product=item.product,
#                     quantity=item.quantity,
#                     address=Address.objects.filter(user=user).latest('id'),  # Assuming the latest address is used
#                     total=item.total_cost
#                 )
#                 order.save()

#                 # Update the stock
#                 item.product.stock -= item.quantity
#                 if item.product.stock <= 0:
#                     item.product.is_stock = False
#                 item.product.save()

#             # Clear the cart after the order is placed
#             cart_items.delete()

#         messages.success(request, "Your order has been placed successfully and the cart has been cleared.")
#         return redirect('order')  # Redirect to an order summary page or similar
#     else:
#         messages.error(request, "Invalid request.")
#         return redirect('/cart')
    

def placeorder(request):
    if request.method == 'GET':
        user = request.user
        address = Address.objects.filter(user=user).latest('id')
        # if addresses.count() > 3:
        #     fourth_address = addresses[3]
        # else:
        #     fourth_address = None
        cart_items = Cart.objects.filter(user=user)
        if not cart_items:
            # messages.error(request, "There is nothing in your cart to place an order.")
            return redirect('index')

        order = Order(user=user,address=address)
        total_price = 0

        for item in cart_items:
            total_price += item.quantity * item.product.discounted_price
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        order.total = total_price + 40  # Assuming 40 is some additional charge
        order.save()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price
            )
        cart_items.delete()
        # Clear the cart after placing the order

       
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_SECRET_KEY))
        payment = client.order.create({
            'amount': int(order.total * 100),  # Razorpay expects the amount in the smallest currency unit (paise)
            'currency': 'INR',
            'payment_capture': '1'
        })
        context = {
            'order_id': payment['id'],
            'amount': int(order.total * 100),  # Make sure to pass the correct amount for the payment
            'user_name': user.username,
            'payment' :payment,
            'address' : address,
        }
        order.razorpay_order_id = payment['id']
        order_obj = Order.objects.filter(user=user).latest('id')
        subject = 'Order Confirmation'
        message = f'''Hello {order_obj.user.username}, \nYour Order is confirmed & your total purchase amount is {order_obj.total} . Your order will be delivered soon. \nThank you for visiting SmartLook.'''
        email_from = settings.EMAIL_HOST_USER
        #recipient_list = [Appointment.email]
        recipient_list = [order_obj.user.email,]
        send_mail( subject, message, email_from, recipient_list,fail_silently=False )
        messages.success(request,"Your Order is placed.\n Check your mail for confirmation..!!")
        
        if not cart_items:
            # messages.error(request, "There is nothing in your cart to place an order.")
            return redirect('index')


    return redirect(reverse('placeorder',context))  
    
    # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_SECRET_KEY))
    #     payment = client.order.create({'amount': int(order.total * 100),"currency": "INR",'payment_capture' : 1})
    #     order.razorpay_order_id = payment['id']
    #     order.save()
    #     context = {'payment' : payment,'order':order}
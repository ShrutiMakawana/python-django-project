from django.contrib import admin

from app1.models import Appointment, Contact,Employee,Service,Gallery,Product,Profile,Cart,Address,Order,OrderItem

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','message']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user','name','service','date','slot','appointment_status']
    list_editable = ['name','appointment_status']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'name','designation','description','image']
    list_editable = ['name','designation','description','image']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service_name','category']
    list_editable = ['service_name','category']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id','glr_image']
    list_editable = ['glr_image']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pro_id','name','image','discounted_price','category','stock','is_stock']
    list_editable = ['name','image','discounted_price','category','stock','is_stock']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','created_at','token']

    
# @admin.register(Cart)
# class CartModelAdmin(admin.ModelAdmin):
#     list_display=['id','user','product','quantity']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display=['id','user','address','city','pincode','mobileno','payment_method']

# @admin.register(Payment)
# class PaymentModelAdmin(admin.ModelAdmin):
#     list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid',]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','total','status','created_at','address']
    list_editable=['status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','price']


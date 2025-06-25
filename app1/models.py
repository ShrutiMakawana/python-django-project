from django.db import models,transaction
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=20)
    message = models.TextField()
    date = models.DateField()

class Appointment(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    #user = models.IntegerField(null=True)
    user = models.CharField(max_length=10,null=True)
    #service_id=models.ForeignKey(Service,default=1,verbose_name="service", on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=70,default='')
    age = models.IntegerField(default=0)
    mobileno = models.CharField(default='',max_length=10)
    email = models.EmailField(default='')
    service = models.CharField(max_length=100,default='')
    category = models.CharField(max_length=100,default='')
    date = models.DateField()
    slot = models.TextField(max_length=20,default='')
    appointment_status = models.BooleanField(default=False)
    # def __str__(self):
    #     return self.id

class Employee(models.Model):
    emp_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=70,default='')
    designation = models.CharField(max_length=120,default='')
    description = models.TextField(max_length=300,default='')
    image = models.ImageField(upload_to='static/assets/img',default='')
    def __str__(self):
        return self.name

class Service(models.Model):
    service_id = models.BigAutoField(primary_key=True)
    service_name = models.CharField(max_length=100,default='')
    category = models.CharField(max_length=100,default='')
    def __str__(self):
        return self.service_name

class Gallery(models.Model):
    glr_image=models.ImageField(upload_to="static/assets/img",default="")
    def __int__(self):
        return self.id   

CATEGORY_CHOICES=(
   ('HR','hair'),
   ('SK','Skin'),
   ('NL','Nail'),
   ('BD','body')

)

class Product(models.Model):
    pro_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200,default="") 
    image = models.ImageField(upload_to="static/assets/img",default='')
    discounted_price = models.DecimalField(default=0, decimal_places=2,max_digits=10)
    description = models.TextField(max_length=200,default='')
    composition = models.TextField(max_length=200,default='',null=True)
    prodapp = models.TextField(max_length=200,default='',null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2,default='') 
    stock = models.IntegerField()
    is_stock = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'

    
    # class Meta:
    #     # Gives the proper plural name for admin
    #     verbose_name_plural = "service"
    # def _str_(self):
    #     return self.service_id

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    @property
    def total_cost(self):
         return self.quantity * self.product.discounted_price


CITY_CHOICES=(
   ('Ahmedabad','Ahmedabad'),
   ('Vadodara','Vadodara'),
   ('Gandhinagar','Gandhinagar'),
   ('Bhavnagar','Bhavnagar'),
   ('Rajkot','Rajkot'),
   ('Bavla','Bavla'),
   ('Amreli','Amreli'),
)
PAY_CHOICES = (
    ('COD','COD'),
    ('Online','Online'),
)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(max_length=200)
    city= models.CharField(max_length=50,choices=CITY_CHOICES)
    state= models.CharField(max_length=20,default='GUJARAT')
    pincode = models.IntegerField()
    mobileno = models.BigIntegerField()
    payment_method = models.CharField(max_length=50,choices=PAY_CHOICES,default='Online')
    def _str_(self):
       return self.user.username



# class Payment(models. Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    amount = models.FloatField()
#    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
#    razorpay_payment_signature = models.CharField(max_length=100, blank=True, null=True)
#    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
#    is_paid = models. BooleanField(default=False)

STATUS_CHOICES = (
      ('Accepted', 'Accepted'),
      ('On The Way', 'On The Way'),
      ('Delivered', 'Delivered'),
      ('Cancel', 'Cancel'),
      ('Pending', 'Pending'),
      )

# class OrderPlaced(models.Model):
#      user= models.ForeignKey(User,on_delete=models.CASCADE)
#      product =models.ForeignKey(Product,on_delete=models.CASCADE)
#      address= models.ForeignKey(Address, on_delete=models.CASCADE)
#      quantity= models. PositiveIntegerField(default=1)
#      total = models.DecimalField(max_digits=100,decimal_places=2)
#      ordered_date = models. DateTimeField(auto_now_add=True)
#      status =models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
# #    payment = models. ForeignKey (Payment, on_delete=models. CASCADE, default="")
#      @property
#      def total_cost(self):
#          return self.quantity * self.product.discounted_price
     

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     address = models.ForeignKey(Address, on_delete=models.CASCADE)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.pk} by {self.user.username}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

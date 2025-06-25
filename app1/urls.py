from django.contrib import admin
from django.urls import path
from app1 import views
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('',views.index1,name='index1'),
    path('index',views.index1,name='index'),
    path('signup',views.signup,name='signup'),
    path('login',views.login_view,name='login'),
    path('userpro',views.userpro,name='userpro'),
    path('cancel_appointment/<int:id>',views.cancel_appointment,name='cancel_appointment'),

    path('saveEnquiry',views.saveEnquiry,name="saveEnquiry"),


    path('logout',views.log_out,name="logout"),
    path('appointmentbooking',views.appointmentbooking,name='appointmentbooking'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('change_password/<token>',views.change_password,name='change_password'),

    # path('password_reset',auth_views.PasswordResetView.as_view(),name='password_reset'),
    # path('password_reset_done',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    #path('cart',views.cart,name='cart'),
    #path('product_detail',views.product_detail,name='product_detail'),  

    path('cart/',views.show_cart,name='showcart'),
    path("add-to-cart/",views.add_to_cart,name='add-to-cart'),

    path('category/<slug:value>',views.CategoryView.as_view(),name='category'),
    path('category-title/<val>',views.CategoryTitle.as_view(),name='category-title'),
    path('product-detail/<int:pk>',views.ProductDetail.as_view(),name='product-detail'),

    path('checkout/address',views.address,name='address'),
    path('order',views.order,name='order'),

    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    
    path('removecart/',views.remove_cart),
    # # path('paymentdone/',views.payment_done,name='paymentdone'),
    # path('orders/',views.index1,name='orders'),

    path('placeorder',views.placeorder,name='placeorder'),



]

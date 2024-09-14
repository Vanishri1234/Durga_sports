"""
URL configuration for my_sports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from sports_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.userlogin, name='userlogin'),

    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),

    path('superadmin',views.superadmin,name='superadmin'),


    path('register/', views.register, name='register'),
    path('register_form/<int:admission_no>', views.register_form, name='register_form'),

    path('admission_list/', views.admission_list, name='admission_list'),
    path('edit/<int:pk>/', views.edit_admission, name='edit_admission'),
    path('delete/<int:pk>/', views.delete_admission, name='delete_admission'),

    path('enquiry_form/', views.enquiry_form, name='enquiry_form'),
    path('enquiry_list', views.enquiry_list, name='enquiry_list'),
    path('edit-enquiry/<int:id>/', views.edit_enquiry, name='edit_enquiry'),
    path('delete/<int:pk>/', views.delete_enquiry, name='delete_enquiry'),

    path('sessions', views.sessions, name='sessions'),
    path('receipt/<int:admission_no>', views.receipt, name='receipt'),

    path('coach_reg', views.coach_reg, name='coach_reg'),

    path('player_name/', views.player_name, name='player_name'),
    path('coach_allocation/', views.coach_allocation, name='coach_allocation'),

    path('fetch-name-data/', views.fetch_name_data, name='fetch_name_data'),
    path('fetch_coach_data/', views.fetch_coach_data, name='fetch_coach_data'),

    path('kit-entry/', views.kit_entry, name='kit_entry'),
    path('kit-list/', views.kit_list, name='kit_list'),
    path('edit-kit/<int:kit_id>/', views.edit_kit, name='edit_kit'),
    path('delete-kit/<int:kit_id>/', views.delete_kit, name='delete_kit'),

    path('item-entry/', views.item_entry, name='item_entry'),
    path('item_list/', views.item_list, name='item_list'),
    path('edit-item/<int:id>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:id>/', views.delete_item, name='delete_item'),

    path('kit_dist/', views.kit_dist, name='kit_dist'),
    path('player_details/', views.player_details, name='player_details'),

    path('fetch_kit_list/', views.fetch_kit_list, name='fetch_kit_list'),
    path('fetch_item_list/', views.fetch_item_list, name='fetch_item_list'),

    path('kit_distribution_view/', views.kit_distribution_view, name='kit_distribution_view'),

    path('get_coach_type/<int:coach_id>/', views.get_coach_type, name='get_coach_type'),

    path('dist_receipt/<int:receipt>', views.dist_receipt, name='dist_receipt'),

    path('coach_list', views.coach_list, name='coach_list'),

    path('edit-coach/<int:id>/', views.edit_coach, name='edit_coach'),

    path('delete/<int:pk>/', views.delete_coach, name='delete_coach'),

    path('purchase/', views.purchase_kit, name='purchase_kit'),
    path('product_dist/', views.product_dist, name='product_dist'),
    path('get_player/', views.get_player, name='get_player'),



    path('purchase_list/', views.purchase_kit_list, name='purchase_kit_list'),

    path('item-purchase/', views.item_purchase, name='item_purchase'),
    path('item-purchase-list/', views.item_purchase_list, name='item_purchase_list'),


    path('company_details/', views.company_details, name='company_details'),
    path('suppliers/', views.supplier_list, name='supplier_list'),

    path('customer', views.customer, name='customer'),

    path('customer_list', views.customer_list, name='customer_list'),

    path('edit_customer/<int:id>/', views.edit_customer, name='edit_customer'),

    path('customer_prod_dist/', views.customer_prod_dist, name='customer_prod_dist'),
    path('customer_dist_receipt/<int:receipt>', views.customer_dist_receipt, name='customer_dist_receipt'),

    path('customer_sale_list/', views.customer_sale_list, name='customer_sale_list'),
    path('player_sale_list/', views.player_sale_list, name='player_sale_list'),



    path('player_attendence/', views.player_attendence, name='player_attendence'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('store/', views.store_list, name='store_list'),
    path('coach_attendence/', views.coach_attendence, name='coach_attendence'),
    path('coach_attendance_list/', views.coach_attendance_list, name='coach_attendance_list'),


















]

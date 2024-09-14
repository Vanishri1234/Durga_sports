import datetime
import json
import random
from collections import defaultdict
from urllib import request

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.checks import messages
from django.db import transaction
from django.db.models import Sum, Count, Q, When
from django.db.models.functions import ExtractYear, ExtractMonth
from django.forms import IntegerField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from sqlparse.sql import Case

from .forms import EnquiryForm, RegisterForm, CoachForm, PurchaseForm, KitPurchaseForm, ItemPurchaseForm, SupplierForm, \
    CustomerForm
from .models import Enquiry, AddRegister, Duration, coachReg, Coach_allocation, KitItem, Item_entry, kit_distribution, \
    Purchase, KitPurchase, ItemPurchase, Company, Store, Stock, Sale, Customer, Customer_sale, Userlogin, Login, \
    Attendence, Coach_Attendence


# Create your views here.

def admin(request):
    return render(request,"admin.html")


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('t1')
        password = request.POST.get('t2')
        request.session['username'] = username
        ucount = Login.objects.filter(username=username).count()
        if ucount >= 1:
            udata = Login.objects.get(username=username)
            upass = udata.password
            utype = udata.utype
            if password == upass:
                request.session['utype'] = utype
                if utype == 'user':
                    return render(request, 'index.html')
                if utype == 'admin':
                    return render(request, 'home.html')
                if utype == 'coach':
                    return render(request, 'coach_home.html')
                if utype == 'superadmin':
                    return render(request, 'superadmin.html')
            else:
                return render(request, 'userlogin.html', {'msg': 'Invalid Password'})
        else:
            return render(request, 'userlogin.html', {'msg': 'Invalid Username'})
    return render(request, 'userlogin.html')


def superadmin(request):
    return render(request,'superadmin.html')
def index(request):
    return render(request,'index.html')

#Enquiry
def enquiry_form(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        date_of_birth = request.POST.get('dateOfBirth')
        gender = request.POST.get('gender')
        contact_no = request.POST.get('contactNo')
        parent_name = request.POST.get('parentName')
        parent_mobile_no = request.POST.get('parentMobileNo')
        parent_email = request.POST.get('parentEmail')
        parent_address = request.POST.get('parentAddress')
        weekly_sessions = request.POST.get('weeklySessions')
        how_did_you_know = request.POST.get('howDidYouKnow')
        other_details = request.POST.get('otherDetails')
        age = request.POST.get('age')


        # Calculate age based on date of birth


        # Save the data to the database (assuming you have a model named Enquiry)
        enquiry = Enquiry(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            contact_no=contact_no,
            parent_name=parent_name,
            parent_mobile_no=parent_mobile_no,
            parent_email=parent_email,
            parent_address=parent_address,
            weekly_sessions=weekly_sessions,
            how_did_you_know=how_did_you_know,
            other_details=other_details,
            age=age,

        )
        enquiry.save()

        # Redirect after successful form submission (optional)
        return redirect('enquiry_list')

    # Render the form template if it's a GET request
    return render(request, 'Enquiry/players_enquiry.html')

def player_list(request):
    enquiries=Enquiry.objects.all()
    return render(request,'Enquiry/player_list.html',{'enquiries':enquiries})

def enquiry_list(request):
    search_query = request.GET.get('q', '')
    search_age = request.GET.get('age', '')
    search_mobile = request.GET.get('mobile', '')
    search_gender = request.GET.get('gender', '')

    enquiries = Enquiry.objects.all()

    if search_query:
        enquiries = enquiries.filter(first_name__icontains=search_query)
    if search_age:
        enquiries = enquiries.filter(age=search_age)
    if search_mobile:
        enquiries = enquiries.filter(contact_no__icontains=search_mobile)
    if search_gender:
        enquiries = enquiries.filter(gender__iexact=search_gender)

    context = {
        'data': enquiries,
    }
    return render(request, 'Enquiry/enquiry_list.html', context)

def edit_enquiry(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)
    if request.method == 'POST':
        form = EnquiryForm(request.POST, instance=enquiry)
        if form.is_valid():
            form.save()
            return redirect('enquiry_list')
    else:
        form = EnquiryForm(instance=enquiry)
    return render(request, 'Enquiry/edit_enquiry.html', {'form': form})


def purchase_kit(request):
    if request.method == 'POST':
        item_id = request.POST.get('item')
        quantity = int(request.POST.get('quantity'))

        try:
            item = KitItem.objects.get(pk=item_id)
            total_price = item.unit_price * quantity

            # Handle the purchase transaction
            with transaction.atomic():
                purchase = Purchase(item=item, quantity=quantity, total_price=total_price)
                purchase.save()

            # Add a success message to be displayed
            messages.add_message(request, messages.SUCCESS, f'Purchase successful! Total price: ${total_price:.2f}')
        except KitItem.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Item does not exist.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'An error occurred: {str(e)}')

        return redirect('purchase_kit')

    # If GET request, render the form to purchase a kit
    items = KitItem.objects.all()
    return render(request, 'stock/purchase_kit.html', {'items': items})


def delete_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        enquiry.delete()
        return redirect('enquiry_list')  # Redirect to the list view

    return render(request, 'confirm_delete.html', {'enquiry': enquiry})




def register(request):
    if request.method == "POST":

        now = datetime.datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        admission_no = random.randint(1111, 9999)
        adm_no = str(admission_no)

        invoice_ID = random.randint(1111, 9999)
        invoice = str(invoice_ID)

        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        adhar = request.POST.get('adhar')
        parentName = request.POST.get('parentName')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        place = request.POST.get('place')
        address = request.POST.get('address')
        uniformSize = request.POST.get('uniformSize')
        uniformColor = request.POST.get('uniformColor')
        package = request.POST.get('package')
        sessions = request.POST.get('sessions')
        totalAmount = request.POST.get('totalAmount')
        blood_group = request.POST.get('blood_group')
        payment = request.POST.get('payment')
        balance = request.POST.get('balance')
        batchtime = request.POST.get('batchtime')
        name = request.POST.get('name')
        doj = request.POST.get('doj')
        age = request.POST.get('age')

        AddRegister.objects.create(
            admission_no=adm_no,
            date=con_date,
            dob=dob,
            gender=gender,
            phone=phone,
            adhar=adhar,
            parentName=parentName,
            mobile=mobile,
            email=email,
            place=place,
            address=address,
            uniformSize=uniformSize,
            uniformColor=uniformColor,
            package=package,
            sessions=sessions,
            totalAmount=totalAmount,
            invoice_ID=invoice,
            blood_group=blood_group,
            payment=payment,
            balance=balance,
            batchtime=batchtime,
            name=name,
            doj=doj,
            age=age
        )
        return redirect('receipt', admission_no=adm_no)
    return render(request, 'Admission/admission.html')

def fetch_coach_type(request):
    if request.method == 'POST':
        coach_name = request.POST.get('coachname')
        try:
            coach = coachReg.objects.get(coachname=coach_name)
            return JsonResponse({'coachType': coach.coachtype})
        except coachReg.DoesNotExist:
            return JsonResponse({'coachType': ''})
    return JsonResponse({'coachType': ''})

def get_coach_type(request, coach_id):
    try:
        coach = coachReg.objects.get(id=coach_id)
        return JsonResponse({'coachType': coach.coachType})
    except coachReg.DoesNotExist:
        return JsonResponse({'error': 'Coach not found'}, status=404)


def receipt(request,admission_no):
    admission=get_object_or_404(AddRegister,admission_no=admission_no)
    return render(request,'Admission/Recipt.html',{'admission':admission})



def register_form(request,admission_no):
    admission=get_object_or_404(AddRegister,admission_no=admission_no)
    return render(request,'Admission/admission_form.html',{'admission':admission})


def admission_list(request):
    admissions = AddRegister.objects.all()

    mobile = request.GET.get('mobile')
    admission_no = request.GET.get('admission_no')
    gender = request.GET.get('gender')
    age = request.GET.get('age')

    if mobile:
        admissions = admissions.filter(mobile__icontains=mobile)
    if admission_no:
        admissions = admissions.filter(admission_no__icontains=admission_no)
    if gender:
        admissions = admissions.filter(gender=gender)
    if age:
        admissions = admissions.filter(age=age)  # Make sure 'age' is a valid field

    context = {
        'data': admissions
    }
    return render(request, 'Admission/admission_list.html', context)

def edit_admission(request, pk):
    admission = get_object_or_404(AddRegister, id=pk)
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=admission)
        if form.is_valid():
            form.save()
            return redirect('admission_list')
    else:
        form = RegisterForm(instance=admission)
    return render(request, 'Admission/edit_admission.html', {'form': form})




def delete_admission(request, pk):
    admission = get_object_or_404(AddRegister, id=pk)
    if request.method == 'POST':
        admission.delete()
        return redirect('admission_list')
    return render(request, 'admission_list.html', {'data': AddRegister.objects.all()})
def home(request):
    return render(request,"home.html")


def sessions(request):
    if request.method=="POST":
        session=request.POST.get('session')
        weekly=request.POST.get('weeklySessions')
        pay=request.POST.get('amount')

        Duration.objects.create(
            session=session,
            weekly_sessions=weekly,
            amount=pay
        )
        return redirect('sessions')
    return render(request,'Admission/sessions.html')

def duration(request):
    duration = Duration.objects.all()
    return render(request, 'Admission/admission.html', {'duration': duration})


def coach_reg(request):
    if request.method == 'POST':
        # Extract data from the form
        coachname = request.POST.get('coachname')
        adhar=request.POST.get('adhar')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        coachType = request.POST.get('coachType')
        address=request.POST.get('address')
        document=request.POST.get('document')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        utype = 'coach'

        coachReg.objects.create(
            coachname=coachname,
            email=email,
            phone=phone,
            coachType=coachType,
            adhar=adhar,
            address=address,
            document=document,
            gender=gender,
            password=password,

        )
        Login.objects.create(utype=utype, username=phone, password=password)
        return redirect('coach_list')
    return render(request, 'coaches/coach_Reg.html')




def player_name(request):
    rName = AddRegister.objects.all()
    cName = coachReg.objects.all()
    return render(request, 'coaches/coach_allocation.html', {'rName': rName, 'cName': cName})


def coach_allocation(request):
    if request.method == 'POST':
        # Extract data from the form

        session = request.POST.get('session')
        batchtime = request.POST.get('batchtime')
        coachname = request.POST.get('coachname')
        coachType = request.POST.get('coachType')


        Coach_allocation.objects.create(
            session=session,
            batchtime=batchtime,
            coachname=coachname,
            coachType=coachType

        )

        return redirect('coach_allocation')
    return render(request, 'coaches/coach_allocation.html')


def fetch_name_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            player = get_object_or_404(AddRegister, name=name)
            data = {

                'session': player.sessions,
                'batchtime':player.batchtime
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid  name'})
    return JsonResponse({'error': 'Invalid request method'})

def fetch_coach_data(request):
    if request.method == 'POST':
        coachname = request.POST.get('coachname')
        if coachname:
            coach = get_object_or_404(coachReg, coachname=coachname)
            data = {
                'coachType': coach.coachType,

            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid coach name'})
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def kit_entry(request):
    if request.method == "POST":
        brand_names = request.POST.getlist('brand_name[]')
        no_of_stocks = request.POST.getlist('no_of_stock[]')
        unit_prices = request.POST.getlist('unit_price[]')

        for brand_name, no_of_stock, unit_price in zip(brand_names, no_of_stocks, unit_prices):
            KitItem.objects.create(
                brand_name=brand_name,
                no_of_stock=no_of_stock,
                unit_price=unit_price
            )

        return redirect('kit_entry')

    return render(request, 'stock/kit_entry.html')

def kit_list(request):
    kits = KitItem.objects.all()
    return render(request, 'stock/kit_list.html', {'kits': kits})

def edit_kit(request, kit_id):
    kit = get_object_or_404(KitItem, id=kit_id)
    if request.method == "POST":
        kit.brand_name = request.POST.get('brand_name')
        kit.no_of_stock = request.POST.get('no_of_stock')
        kit.unit_price = request.POST.get('unit_price')
        kit.save()
        return redirect('kit_list')

    return render(request, 'stock/edit_kit.html', {'kit': kit})

def delete_kit(request, kit_id):
    kit = get_object_or_404(KitItem, id=kit_id)
    kit.delete()
    return redirect('kit_list')

@csrf_exempt
def item_entry(request):
    if request.method == "POST":
        itemname = request.POST.get('Item_name[]')
        purpose = request.POST.get('purpose[]')
        pieces = request.POST.get('pieces[]')
        price=request.POST.get('price[]')
        Item_entry.objects.create(
                itemname=itemname,
                purpose=purpose,
                pieces=pieces,
                price=price
        )

        return redirect('item_entry')

    return render(request, 'stock/item_entry.html')

def item_list(request):
    items = Item_entry.objects.all()
    return render(request, 'stock/item_list.html', {'items': items})

def edit_item(request, id):
    item = get_object_or_404(Item_entry, id=id)
    if request.method == 'POST':
        item.itemname = request.POST.get('Item_name[]')
        item.pieces = request.POST.get('no_of_pieces')
        item.price = request.POST.get('price')
        item.save()
        return redirect('item_list')
    return render(request, 'stock/edit_item.html', {'item': item})

def delete_item(request, id):
    item = get_object_or_404(Item_entry, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item_list.html')

def kit_dist(request):
    admissions = AddRegister.objects.all()
    return render(request, "stock/kit_dist.html", {'admissions': admissions})


def player_details(request):
    admissions = AddRegister.objects.all()
    selected_player = None

    if 'name' in request.GET:
        selected_player = get_object_or_404(AddRegister, id=request.GET['name'])

    kits = KitItem.objects.all()
    items = Item_entry.objects.all()  # Fetch all items from the Item model

    return render(request, 'stock/kit_dist.html', {
        'admissions': admissions,
        'selected_player': selected_player,
        'kits': kits,
        'items': items  # Pass items to the template
    })

def fetch_kit_list(request):
    try:
        kits = KitItem.objects.all().values('name', 'brand_name', 'no_of_stock', 'unit_price')
        return JsonResponse({'kits': list(kits)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def fetch_item_list(request):
    items = Item_entry.objects.all().values('id', 'itemname', 'pieces', 'price')
    item_list = list(items)
    return JsonResponse({'items': item_list})




def kit_distribution_view(request):
    admissions = AddRegister.objects.all()
    selected_player = None
    receipt = None  # Initialize receipt with a default value

    if request.method == 'GET' and 'name' in request.GET:
        selected_player_id = request.GET.get('name')
        if selected_player_id:
            selected_player = AddRegister.objects.get(id=selected_player_id)
            receipt_ID = random.randint(1111, 9999)
            receipt = str(receipt_ID)

    if request.method == 'POST':
        selectCustomer = request.POST.get('selectCustomer')
        admission_no = request.POST.get('admission_no')
        phone = request.POST.get('phone')
        adhar = request.POST.get('adhar')
        place = request.POST.get('place')
        address = request.POST.get('address')
        package = request.POST.get('package')
        sessions = request.POST.get('sessions')
        batchtime = request.POST.get('batchtime')
        totalAmount = request.POST.get('totalAmount')
        balance = request.POST.get('balance')
        brand_name = request.POST.get('brand_name')

        # Handle possible empty strings for integer conversion
        def safe_int(value, default=0):
            try:
                return int(value)
            except ValueError:
                return default

        kit_quantity = safe_int(request.POST.get('kit_quantity', ''))
        kitTotalAmount = request.POST.get('kitTotalAmount')
        finalAmount = request.POST.get('finalAmount')
        kit_id = request.POST.get('kit_id')
        item_id = request.POST.get('item_id')
        itemname = request.POST.get('itemname')
        item_quantity = safe_int(request.POST.get('item_quantity', ''))
        itemTotalAmount = request.POST.get('itemTotalAmount')
        name = request.POST.get('name')
        unit_price = request.POST.get('unit_price')
        price = request.POST.get('price')

        if not receipt:
            receipt_ID = random.randint(1111, 9999)
            receipt = str(receipt_ID)

        if selectCustomer:
            kit_distribution.objects.create(
                selectCustomer=selectCustomer,
                admission_no=admission_no,
                phone=phone,
                adhar=adhar,
                place=place,
                address=address,
                package=package,
                sessions=sessions,
                batchtime=batchtime,
                totalAmount=totalAmount,
                balance=balance,
                brand_name=brand_name,
                kit_quantity=kit_quantity,
                kitTotalAmount=kitTotalAmount,
                finalAmount=finalAmount,
                kit=kit_id,
                item=item_id,
                itemname=itemname,
                item_quantity=item_quantity,
                itemTotalAmount=itemTotalAmount,
                name=name,
                unit_price=unit_price,
                price=price,
                receipt=receipt
            )

            # Update Kit Stock
            if kit_id:
                try:
                    kit = Store.objects.get(id=kit_id)
                    if kit.no_of_stock >= kit_quantity:
                        kit.no_of_stock -= kit_quantity
                        kit.save()
                except Store.DoesNotExist:
                    pass

            # Update Item Stock
            if item_id:
                try:
                    item = Item_entry.objects.get(id=item_id)
                    if item.pieces >= item_quantity:
                        item.pieces -= item_quantity
                        item.save()
                except Item_entry.DoesNotExist:
                    pass

            return redirect('dist_receipt',receipt=receipt)


    context = {
        'admissions': admissions,
        'selected_player': selected_player,
    }

    return render(request, 'stock/kit_dist.html', context)
def dist_receipt(request,receipt):
    admission=get_object_or_404(Sale,receipt=receipt)
    return render(request,'stock/dist_receipt.html',{'admission':admission})




def coach_list(request):
    # Extract query parameters
    query = request.GET.get('q', '')
    phone = request.GET.get('phone', '')
    gender = request.GET.get('gender', '')

    # Filter coaches based on query parameters
    coaches = coachReg.objects.all()
    if query:
        coaches = coaches.filter(coachname__icontains=query)
    if phone:
        coaches = coaches.filter(phone__icontains=phone)
    if gender:
        coaches = coaches.filter(gender=gender)

    context = {
        'data': coaches,
    }

    return render(request, 'Coaches/coach_list.html', context)






def edit_coach(request, id):
    coach = get_object_or_404(coachReg, id=id)
    if request.method == 'POST':
        form = CoachForm(request.POST, instance=coach)
        if form.is_valid():
            form.save()
            return redirect('coach_list')
    else:
        form = CoachForm(instance=coach)
    return render(request, 'coaches/edit_coach.html', {'form': form})


def delete_coach(request, pk):
    coach = get_object_or_404(coachReg, pk=pk)
    if request.method == 'POST':
        coach.delete()
        return redirect('coach_list')  # Redirect to the list view

    return render(request, 'confirm_delete.html', {'coach': coach})


def purchase_kit(request):
    if request.method == "POST":
        company_id = request.POST.get('company')
        date = request.POST.get('date')
        total_cost = request.POST.get('total_cost')

        company = Company.objects.get(id=company_id)

        # Create lists of KitPurchase and Store objects
        kits = []
        stocks = []
        i = 1

        while True:
            kit_name = request.POST.get(f'kit_name_{i}')
            if not kit_name:
                break
            quantity = request.POST.get(f'quantity_{i}')
            price_per_unit = request.POST.get(f'price_per_unit_{i}')
            description = request.POST.get(f'description_{i}')

            total_cost = round(float(quantity) * float(price_per_unit), 2)

            kits.append(KitPurchase(
                kit_name=kit_name,
                quantity=quantity,
                price_per_unit=price_per_unit,
                total_cost=total_cost,
                description=description,
                company_name=company.comapny_name,  # Updated attribute
                date=date
            ))

            stocks.append(Store(
                kit_name=kit_name,
                quantity=quantity,
                price_per_unit=price_per_unit,
                total_cost=total_cost,
                description=description,
                company_name=company.comapny_name,  # Updated attribute
                date=date
            ))

            i += 1

        # Bulk create KitPurchase and Store entries
        KitPurchase.objects.bulk_create(kits)
        Store.objects.bulk_create(stocks)

        return redirect('purchase_kit_list')

    # Handle GET request
    companies = Company.objects.all()
    return render(request, 'stock/purchase.html', {'companies': companies})

def  purchase_kit_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    purchases = KitPurchase.objects.all()


    if start_date:
        start_date = parse_date(start_date)
        purchases = purchases.filter(date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        purchases = purchases.filter(date__lte=end_date)

    return render(request, 'stock/purchase_kit_list.html', {'purchases': purchases})

def item_purchase(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price_per_unit = request.POST.get('price_per_unit')
        total_cost = request.POST.get('total_cost')
        company_id = request.POST.get('company')
        date=request.POST.get('date')

        company = Company.objects.get(id=company_id)

        ItemPurchase.objects.create(
            item_name=item_name,
            description=description,
            quantity=quantity,
            price_per_unit=price_per_unit,
            total_cost=total_cost,
            company_name=company.comapny_name,
            date=date# Updated to reflect the actual field
        )

        return redirect('item_purchase_list')

    companies = Company.objects.all()
    return render(request, 'stock/item_purchase.html', {'companies': companies})

def item_purchase_list(request):
    purchases = ItemPurchase.objects.all()
    return render(request, 'stock/item_purchase_list.html', {'purchases': purchases})


def company_details(request):
    if request.method == "POST":
        comapny_name = request.POST.get('comapny_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email=request.POST.get('email')
        other_details = request.POST.get('other_details')
        Company.objects.create(
                comapny_name=comapny_name,
                address=address,
                phone_number=phone_number,
                email=email,
                other_details=other_details
        )

        return redirect('company_details')

    return render(request, 'stock/supplier_form.html')


def supplier_list(request):
    suppliers = Company.objects.all()  # Fetch all suppliers from the database
    return render(request, 'stock/supplier_list.html', {'suppliers': suppliers})


def product_dist(request):
    names = AddRegister.objects.values_list('name', flat=True)
    products = Store.objects.all()
    details = None
    product_details = None
    receipt = None

    # Filter based on name or id as needed
    if 'name' in request.GET:
        name = request.GET['name']
        details = AddRegister.objects.filter(name=name).first()
        receipt_ID = random.randint(1111, 9999)
        receipt = str(receipt_ID)
        # Filtering by name

    if 'product_id' in request.GET and details:
        try:
            product_id = int(request.GET['product_id'])
            product_details = Store.objects.filter(id=product_id).first()  # Filtering by id
        except ValueError:
            product_details = None

    if request.method == 'POST':
        name = request.POST.get('name')
        admission_no = request.POST.get('admission_no')
        phone = request.POST.get('phone')
        adhar = request.POST.get('adhar')
        place = request.POST.get('place')
        address = request.POST.get('address')
        package = request.POST.get('package')
        sessions = request.POST.get('sessions')
        batchtime = request.POST.get('batchtime')
        quantity = int(request.POST.get('quantity', '0'))
        price_per_unit = float(request.POST.get('price_per_unit', '0'))
        totalCost = float(request.POST.get('totalAmount', '0'))
        updatedBalance = float(request.POST.get('updatedBalance', '0'))
        kit_name = request.POST.get('kit_name')
        balance = request.POST.get('balance')



        if not receipt:
            receipt_ID = random.randint(1111, 9999)
            receipt = str(receipt_ID)

        # Save the sale record
        sale = Sale.objects.create(
            name=name,
            admission_no=admission_no,
            phone=phone,
            adhar=adhar,
            place=place,
            address=address,
            package=package,
            sessions=sessions,
            batchtime=batchtime,
            quantity=quantity,
            price_per_unit=price_per_unit,
            totalCost=totalCost,
            updatedBalance=updatedBalance,
            receipt=receipt,
            kit_name=kit_name,
            balance=balance
        )

        # Update the store quantitycdd
        if product_details:
            product_details.quantity = max(0, product_details.quantity - quantity)
            product_details.save()

        return redirect('dist_receipt',receipt=receipt)  # Adjust to your URL name

    return render(request, 'stock/product_dist.html', {
        'names': names,
        'details': details,
        'products': products,
        'product_details': product_details
    })
def get_player(request):
    query = request.GET.get('query', '')
    if query:
        name = AddRegister.objects.filter(companyname__icontains=query).values_list('name', flat=True)
        print('player Name:', list(name))  # Debugging: check the data in the terminal
        return JsonResponse(list(name), safe=False)
    return JsonResponse([], safe=False)

def customer(request):
    if request.method == 'POST':
        # Extract data from the form
        full_name = request.POST.get('full_name')
        phone_number=request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')


        Customer.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            address=address,
            city=city,


        )
        return redirect('customer_list')
    return render(request, 'stock/customer.html')


def customer_list(request):
    # Get search query parameters
    search_name = request.GET.get('name', '')
    search_age = request.GET.get('age', '')
    search_contact = request.GET.get('contact', '')

    # Filter customers based on search parameters
    customers = Customer.objects.all()
    if search_name:
        customers = customers.filter(full_name__icontains=search_name)
    if search_age:
        customers = customers.filter(age=search_age)
    if search_contact:
        customers = customers.filter(phone_number__icontains=search_contact)

    return render(request, 'stock/customer_list.html', {
        'customers': customers,
        'search_name': search_name,
        'search_age': search_age,
        'search_contact': search_contact
    })


def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'stock/edit_customer.html', {'form': form})




def customer_prod_dist(request):
    # Get customer and product IDs from GET parameters
    customer_id = request.GET.get('customer_id')
    product_id = request.GET.get('product_id')

    # Initialize context dictionary
    context = {
        'customers': Customer.objects.all(),  # For dropdown list of customers
        'products': Store.objects.all(),    # For dropdown list of products
    }

    # Fetch the selected customer details if a customer ID is provided
    if customer_id:
        context['details'] = get_object_or_404(Customer, id=customer_id)

    # Fetch the selected product details if a product ID is provided
    if product_id:
        context['product_details'] = get_object_or_404(Store, id=product_id)

    return render(request, 'stock/customer_prod_dist.html', context)


def customer_prod_dist(request):
    names = Customer.objects.values_list('full_name', flat=True)
    products = Store.objects.all()
    details = None
    product_details = None
    receipt = None

    # Filter based on name or id as needed
    if 'name' in request.GET:
        name = request.GET['name']
        details = Customer.objects.filter(full_name=name).first()
        receipt_ID = random.randint(1111, 9999)
        receipt = str(receipt_ID)

    if 'product_id' in request.GET and details:
        try:
            product_id = int(request.GET['product_id'])
            product_details = Store.objects.filter(id=product_id).first()
        except ValueError:
            product_details = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        kit_name = request.POST.get('kit_name')

        # Handle potential conversion errors
        try:
            quantity = int(request.POST.get('quantity', '0'))
        except ValueError:
            quantity = 0

        try:
            price_per_unit = float(request.POST.get('price_per_unit', '0'))
        except ValueError:
            price_per_unit = 0.0

        try:
            total_cost = float(request.POST.get('totalAmount', '0'))
        except ValueError:
            total_cost = 0.0

        try:
            balance = float(request.POST.get('balance', '0'))
        except ValueError:
            balance = 0.0

        if not receipt:
            receipt_ID = random.randint(1111, 9999)
            receipt = str(receipt_ID)

        # Save the sale record
        sale = Customer_sale.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            address=address,
            city=city,
            kit_name=kit_name,
            quantity=quantity,
            price_per_unit=price_per_unit,
            totalCost=total_cost,
            updatedBalance=balance if balance > 0 else total_cost,
            receipt=receipt
        )

        # Update the store quantity
        if product_details:
            product_details.quantity = max(0, product_details.quantity - quantity)
            product_details.save()

        return redirect('customer_dist_receipt',receipt=receipt)  # Adjust to your URL name

    return render(request, 'stock/customer_prod_dist.html', {
        'names': names,
        'details': details,
        'products': products,
        'product_details': product_details,
    })

def customer_dist_receipt(request,receipt):
    customers=get_object_or_404(Customer_sale,receipt=receipt)
    return render(request,'stock/customer_dist_receipt.html',{'customers':customers})

def customer_sale_list(request):
    # Retrieve search parameters
    search_name = request.GET.get('name', '')
    search_phone = request.GET.get('phone', '')

    # Filter sales based on search parameters
    sales = Customer_sale.objects.all()
    if search_name:
        sales = sales.filter(full_name__icontains=search_name)
    if search_phone:
        sales = sales.filter(phone_number__icontains=search_phone)

    return render(request, 'stock/customer_sale_list.html', {
        'sales': sales,
        'search_name': search_name,
        'search_phone': search_phone,
    })

def customer_sale_receipt(request, receipt_id):
    sale = get_object_or_404(Customer_sale, receipt=receipt_id)
    sale = get_object_or_404(Customer_sale, receipt=receipt_id)
    context = {
        'sale': sale,
    }
    return render(request, 'stock/customer_sale_receipt.html', context)


def player_sale_list(request):
    # Retrieve search parameters
    search_name = request.GET.get('name', '')
    search_sessions = request.GET.get('sessions', '')

    # Filter sales based on search parameters
    sales = Sale.objects.all()
    if search_name:
        sales = sales.filter(name__icontains=search_name)
    if search_sessions:
        sales = sales.filter(sessions__icontains=search_sessions)

    return render(request, 'Admission/player_sale_list.html', {
        'sales': sales,
        'search_name': search_name,
        'search_sessions': search_sessions,
    })


from django.utils import timezone
def player_attendence(request):
    username = request.session.get('username')
    if username:
        try:
            coach = coachReg.objects.get(phone=username)
            name = coach.coachname

            # Retrieve coach allocation details
            coach_det = Coach_allocation.objects.filter(coachname=name).first()
            if coach_det is None:
                return render(request, 'coaches/player_attendence.html', {'msg': 'Coach allocation details not found'})

            session = coach_det.session
            batch = coach_det.batchtime

            # Retrieve players for the session and batch time
            players = AddRegister.objects.filter(sessions=session, batchtime=batch)
            if not players:
                return render(request, 'coaches/player_attendence.html', {'msg': 'No players found for the given session and batch time'})

            # Compute attendance counts
            player_counts = {}
            for player in players:
                present_count = Attendence.objects.filter(name=player.name, status='present').count()
                absent_count = Attendence.objects.filter(name=player.name, status='absent').count()
                player_counts[player.id] = {
                    'present_count': present_count,
                    'absent_count': absent_count,
                }

            context = {
                'coach': coach,
                'players': players,
                'player_counts': player_counts,
                'current_date': timezone.now().strftime('%Y-%m-%d'),
                'total_present': request.session.get('total_present', 0),
                'total_absent': request.session.get('total_absent', 0)
            }
            return render(request, 'coaches/player_attendence.html', context)

        except coachReg.DoesNotExist:
            return render(request, 'coaches/player_attendence.html', {'msg': 'Coach details not found'})
    else:
        return render(request, 'userlogin.html', {'msg': 'Please log in first'})

def submit_attendance(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if username:
            try:
                coach = coachReg.objects.get(phone=username)
                coachType = coach.coachType
                current_date = timezone.now().strftime('%Y-%m-%d')

                total_present = 0
                total_absent = 0

                for key, status in request.POST.items():
                    if key.startswith('attendance-'):
                        player_id = key.split('-')[1]
                        try:
                            player = AddRegister.objects.get(id=player_id)

                            if status == 'present':
                                total_present += 1
                            elif status == 'absent':
                                total_absent += 1

                            Attendence.objects.create(
                                coachname=coach.coachname,
                                coachType=coachType,
                                current_date=current_date,
                                name=player.name,
                                sessions=player.sessions,
                                address=player.address,
                                batchtime=player.batchtime,
                                status=status  # Save status as 'present' or 'absent'
                            )
                        except AddRegister.DoesNotExist:
                            pass  # Handle player not found case

                # Store the counts in the session
                request.session['total_present'] = total_present
                request.session['total_absent'] = total_absent

            except coachReg.DoesNotExist:
                pass  # Optionally handle the case where the coach record doesn't exist

            return redirect('attendance_list')
    return redirect('player_attendance')


def attendance_list(request):
    # Retrieve start_date and end_date from GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    name_filter = request.GET.get('name')

    if start_date and end_date:
        # Parse dates
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        # Filter records by date range
        attendances = Attendence.objects.filter(current_date__range=(start_date, end_date))
    else:
        # If no dates are provided, show all records
        attendances = Attendence.objects.all()

    # Calculate counts for present and absent
    present_count = attendances.filter(status='Present').count()
    absent_count = attendances.filter(status='Absent').count()

    # Aggregate counts per name
    name_counts = Attendence.objects.values('name').annotate(
        present_count=Count('id', filter=Q(status='Present')),
        absent_count=Count('id', filter=Q(status='Absent'))
    )

    # Handle the specific name filter
    if name_filter:
        # Filter attendance records by specific name
        filtered_attendances = attendances.filter(name=name_filter)
        # Aggregate counts by month and year for the specific name
        monthly_name_attendance = (
            filtered_attendances
            .extra({'month': 'EXTRACT(MONTH FROM current_date)', 'year': 'EXTRACT(YEAR FROM current_date)'})
            .values('year', 'month')
            .annotate(
                present_count=Count('id', filter=Q(status='Present')),
                absent_count=Count('id', filter=Q(status='Absent'))
            )
            .order_by('year', 'month')
        )
    else:
        monthly_name_attendance = []

    return render(request, 'attendance_list.html', {
        'attendances': attendances,
        'present_count': present_count,
        'absent_count': absent_count,
        'name_counts': name_counts,
        'monthly_name_attendance': monthly_name_attendance,
        'name_filter': name_filter,
    })
def store_list(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        # Parse dates
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        # Filter items based on date range
        items = Store.objects.filter(date__range=[from_date, to_date])
    else:
        # Default to showing all items if no date range is specified
        items = Store.objects.all()

    context = {
        'items': items,
    }
    return render(request, 'stock/store_list.html', context)


def coach_attendence(request):
    if request.method == 'POST':
        post_data = request.POST
        current_date = timezone.now().date()

        # Iterate over possible attendance entries
        for key, value in post_data.items():
            if key.startswith('attendance_') and value in ['Present', 'Absent']:
                coach_id = key.split('_')[1]
                try:
                    coach = coachReg.objects.get(id=coach_id)
                    # Create or update the attendance record
                    attendance, created = Coach_Attendence.objects.update_or_create(
                        coachname=coach.coachname,
                        coachType=coach.coachType,
                        current_date=current_date,
                        defaults={'status': value}
                    )
                except coachReg.DoesNotExist:
                    pass
        return redirect('coach_attendance_list')

    coaches = coachReg.objects.all()
    return render(request, 'coaches/coach_attendence.html', {'coaches': coaches, 'current_date': timezone.now().date()})



def coach_attendance_list(request):
    # Retrieve start_date and end_date from GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    name_filter = request.GET.get('coachname')

    if start_date and end_date:
        # Parse dates
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        # Filter records by date range
        attendances = Coach_Attendence.objects.filter(current_date__range=(start_date, end_date))
    else:
        # If no dates are provided, show all records
        attendances = Coach_Attendence.objects.all()

    # Calculate counts for present and absent
    present_count = attendances.filter(status='Present').count()
    absent_count = attendances.filter(status='Absent').count()

    # Aggregate counts per coachname
    name_counts = Coach_Attendence.objects.values('coachname').annotate(
        present_count=Count('id', filter=Q(status='Present')),
        absent_count=Count('id', filter=Q(status='Absent'))
    )

    # Handle the specific name filter
    if name_filter:
        # Filter attendance records by specific name
        filtered_attendances = attendances.filter(coachname=name_filter)
        # Aggregate counts by month and year for the specific name
        monthly_name_attendance = (
            filtered_attendances
            .extra({'month': 'EXTRACT(MONTH FROM current_date)', 'year': 'EXTRACT(YEAR FROM current_date)'})
            .values('year', 'month')
            .annotate(
                present_count=Count('id', filter=Q(status='Present')),
                absent_count=Count('id', filter=Q(status='Absent'))
            )
            .order_by('year', 'month')
        )
    else:
        monthly_name_attendance = []

    return render(request, 'coaches/coach_attendence_list.html', {
        'attendances': attendances,
        'present_count': present_count,
        'absent_count': absent_count,
        'name_counts': name_counts,
        'monthly_name_attendance': monthly_name_attendance,
        'name_filter': name_filter,
    })